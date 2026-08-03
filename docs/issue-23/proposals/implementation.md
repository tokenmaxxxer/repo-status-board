files:
- docs/specs/flows-schema.md
- src/rsb/model.py
- src/rsb/web/dashboard.js
- src/rsb/web/dashboard.css (only if the build finds a gap the existing
  token set doesn't cover — survey found none required)
- test/rsb_tests/fixtures.py
- test/rsb_tests/test_model.py

## Request

`spawn.py flows --json`가 `flows[].plan`(스텝별 역할·완료 상태의 실행
계획)을 실어 보내기 시작했다(on-the-record #189, #197). 이 보드가 그
필드를 소비해 이슈별 실행 계획을 화면에 보여주도록 하고, 겸사겸사
"N flows in progress" 요약 칩이 완료된(delivered/closed) flow까지
세고 있는 집계 결함을 고친다. 로컬 스펙 사본
(`docs/specs/flows-schema.md`)도 `plan` 필드 없이 2026-07-31 기준으로
멈춰 있어 재동기화가 필요하다.

## Constraints

- `schema_version` 1 유지 — additive 변경, rsb 쪽 버전 가드 변경 없음.
- `plan: null`(블록 없음)과 `plan: []`(헤더는 있으나 유효 스텝 없음)은
  구분되는 값 — 어느 한쪽으로 뭉개면 안 됨.
- 스텝-역할 조인(플랜의 role ↔ `flows[].roles`의 loop_state/verdict,
  ↔ `decision_queue`의 대기 PR)은 이 레포 책임(on-the-record #189 D3
  결정) — 공급자 페이로드에 이미 조인된 결과를 기대하지 않는다.
  `dashboard.js`에 이미 존재하는 `findDetail()`이 바로 이 패턴(이슈별
  flow/decision/session/ledger 조인)이라 그 위에 얹는다.
- 기존 33개 pytest 테스트는 계속 통과해야 함(회귀 없음).
- 이 레포에는 JS 테스트 하네스가 없다(`package.json`/`jest`/`node --test`
  전무 — survey §5 확인). 새로 들이는 건 이 이슈 범위 밖의 결정.

## Rationale

**플랜 렌더링 위치 — 상세 패널 vs. 메인 테이블 인라인.** 채택안: 스텝별
역할+done+조인 상태의 전체 목록은 `renderDetailPanel()`(클릭 시 열리는
기존 상세 패널)에, 메인 `flowRows()` 테이블에는 "N/M done" 형태의 압축
요약 컬럼만 추가.

Alternative considered and rejected: 전체 스텝 목록을 `flowRows()` 셀
안에 직접 렌더링. Rejected because — `DataTable`의 기존 관례(각 셀이
배지/mono 텍스트 한 줄, `sessionRows`/`decisionRows` 전부 이 관례를
따름)를 스텝 N개 × 역할 N개짜리 다중 필드 리스트로 깨뜨리면 여러 flow를
한눈에 스캔하는 테이블의 핵심 용도를 해친다. 상세 패널은 이미 이슈별
심화 정보(decision, session, ledger)를 클릭으로 열람하는 자리로 확립돼
있어(issue-13 F3 확정) 같은 패턴을 재사용하는 편이 UI 언어를 늘리지
않는다. 스카우트 결과(GitHub Actions류 step list는 순서대로 나열 + 상태
마커라는 단순한 플랫 리스트, DAG 아님 — `scout-brief.md`)도 이 조인된
리스트가 테이블 셀보다 상세 패널의 세로 목록에 더 맞는다는 판단을
뒷받침한다.

**`stage_derived: false` flow를 "in progress" 집계에 포함할지.** 채택안:
포함(진행중으로 셈).

Alternative considered and rejected: 제외(카운트에서 빼고 "unknown"
취급). Rejected because — `flows-schema.md` §2.2상 종료 상태
(delivered/closed)는 룰북에 매핑이 정의된 잘 알려진 상태이고, 매핑 실패
(raw loop_state)는 정의상 새로 생긴/아직 매핑 안 된 중간 상태일 가능성이
훨씬 높다(종료 상태가 매핑 누락일 개연성은 낮음). 제외를 택하면 실제로
진행 중인 flow가 요약 칩에서 조용히 빠지는데, 이는 이슈가 고치라는
결함(집계가 실제 진행 상황과 어긋남)과 같은 종류의 실패를 반대 방향으로
재생산하는 것 — "많이 센다" 버그를 "안전하게 적게 센다" 버그로 바꾸는
셈이라 기각한다.

**`plan` 필드 추출 시 기본값.** 채택안: `fl.get("plan")`(기본값 없음,
키 없으면 `None`).

Alternative considered and rejected: `roles`/`prs`처럼
`fl.get("plan", [])`. Rejected because — `plan: null`과 `plan: []`은
스펙상 구분되는 값인데 `.get(..., [])` 기본값을 쓰면 키 자체가 없는
구페이로드(마이그레이션 과도기)와 명시적 `null`이 똑같이 `[]`가 되어
두 값 다 실제 `[]`와 구분 불가능해진다.

## What will be done

1. `docs/specs/flows-schema.md` §2.2 재동기화: `flows[].plan` 행(타입
   `array<{step:int, roles:[string], done:bool}> | null`, 파싱 규칙,
   `null` vs `[]` 의미)을 이슈 본문에 확정된 문구대로 추가하고, §7 worked
   example에 `plan` 키를 보탠다. 문서 상단 "as of" 날짜를 오늘로 갱신.
2. `src/rsb/model.py`: `PlanStep` 데이터클래스(`step, roles, done` —
   `FlowRole`과 같은 얕은 shape) 추가. `Flow`에 `plan` 필드 추가.
   `normalize_payload()`의 flow 컴프리헨션에서 `fl.get("plan")`을 읽어
   `None`이면 `None`, 아니면 `PlanStep` 리스트로 변환(빈 리스트는 빈
   리스트인 채로 유지 — `None`과 자동 구분됨). `render.py`는 무변경
   (`_dataclass_to_dict`가 이미 제네릭하게 처리).
3. `src/rsb/web/dashboard.js`:
   - `flowRows()`에 "Plan" 컬럼 추가: `plan === null`이면 기존 상태와
     동일하게 `text-secondary` 자리표시(`—`); `plan === []`이면 구분되는
     문구(`0 steps`); 스텝이 있으면 `${done}/${total} done` 배지(전부
     완료면 `status-success`, 아니면 `status-neutral`).
   - `renderDetailPanel()`/`findDetail()`: `detail.flow.plan`이
     null이 아니면 스텝 순서대로 렌더링하는 섹션 추가. 각 스텝: 스텝
     번호, 역할(같은 스텝의 병렬 역할은 한 줄에), done 배지, 그리고
     스텝의 각 역할명을 `detail.flow.roles`에서 찾아 loop_state/verdict를
     붙이고, `data.decisions`에서 `(issue, repo, role)` 일치 항목을 찾아
     대기 중 PR/awaiting을 붙인다(둘 다 없으면 역할명만 표시 — 보드
     레코드 없는 plan-only 이슈가 이 경로를 자연히 탄다).
   - `selectSummary()`: `flows` 칩 카운트를 `stage ∈
     {proposal, approved, implementing} OR stage_derived === false`로
     필터링해 delivered/closed만 제외하도록 수정.
4. `test/rsb_tests/fixtures.py` + `test_model.py`: `plan: null`,
   `plan: []`, 병렬 역할이 있는 다중 스텝 `plan` 각각의 정규화를
   커버하는 픽스처/테스트 추가(기존 `WORKED_EXAMPLE`류 옆에).
5. 수동 검증(phase 2, JS 하네스 부재 — Constraints 참조): issue-13
   선례와 동일하게 `run_server()` + 커스텀 `fetch_board_fn`을 던웨이
   스크립트로 띄워 `plan: null`/`[]`/steps-with-parallel-roles 세
   페이로드를 각각 렌더링해 스텝 순서·역할·done·조인·집계 칩 값을 직접
   확인.

## Out of scope

- `src/rsb/render.py`(CLI 텍스트 렌더러)에 plan 렌더링 추가 — 이슈의
  터치포인트/수용기준 어디에도 CLI 출력이 없음(대시보드 전용 요구).
- 새 JS 테스트 하네스(jest 등) 도입 — 레포 전역 결정이라 이 이슈 범위
  밖(survey §5).
- `hygiene`/`sessions`/`ledger` 섹션 등 plan과 무관한 다른 스펙 드리프트
  재동기화 — §2.2(`plan`)만 재동기화 대상, 다른 섹션은 이슈가 건드리지
  않음.

## How you'll know it worked

- `python3 -m pytest test/ -q` — 기존 테스트 전부 통과 + 새 `plan`
  정규화 테스트 통과.
- `docs/specs/flows-schema.md` §2.2/§7이 이슈 본문에 확정된 `plan` 계약과
  문구 단위로 일치, as-of 날짜 갱신됨.
- 던웨이 스크립트로 세 가지 페이로드(plan null / [] / steps-with-parallel)
  각각 렌더링해 육안 확인: 스텝 순서·역할·done 상태가 상세 패널에
  보이고, 각 스텝 역할에 loop_state/verdict 및 대기 PR이 조인되어
  표시되며, plan-only(보드 레코드 없음) 이슈도 같은 경로로 정상 렌더됨.
- 요약 칩 "N flows in progress"가 delivered/closed 제외, raw
  loop_state(stage_derived:false) 포함 기준으로 정확히 셈 —
  `RAW_STAGE_PAYLOAD` 스타일 픽스처로 확인.
- 수용 기준 6개 항목 모두 커밋 diff/문서에서 추적 가능.
