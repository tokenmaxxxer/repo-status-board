# issue-61 scout brief

survey §7이 남긴 열린 설계 결정("요구사항 1의 가드 위치")에 대한 짧은
스카우팅. `WebSearch` 2회(jsdom/`matchMedia` 커뮤니티 관례, MDN 자체
가이드) — 이 결정은 매우 잘 다져진 영역(모든 주요 테스트 러너
문서화)이라 깊은 리서치가 필요 없다고 판단, 2회로 종료.

## 검토한 패턴 3가지

1. **호출부 인라인 feature-detection** — `typeof window.matchMedia ===
   "function" ? window.matchMedia(q).matches : fallback`. MDN이 SSR/비
   브라우저 환경 전반에 대해 권장하는 정확히 이 형태다: "you would
   typically need to check if `window` is defined before calling
   `matchMedia()`... `if (typeof window !== 'undefined' && window.matchMedia)
   { ... }`"(MDN `Window.matchMedia()`/feature-detection 가이드 요약,
   검색 결과 기준). survey §1의 스파이크가 이미 이 형태로 9/9,
   66/66 green을 실측 확인했다.
2. **테스트 하네스에서 `matchMedia` 스텁 주입** — Jest/Vitest 생태계의
   압도적으로 흔한 해법(`jest.setup.js`의 `Object.defineProperty(window,
   'matchMedia', ...)`, Vitest의 `vi.hoisted()`/`setupFiles` 패턴).
   jsdom이 `matchMedia`를 구현하지 않는다는 사실 자체가 여러 프레임워크
   문서·이슈 트래커(ant-design #21096, Jest manual mocks 문서 등)에
   반복적으로 등장할 만큼 잘 알려진 하네스 공백이다. 이슈 #61 본문도
   이 옵션을 "하네스 matchMedia 스텁"으로 명시적으로 병기한다.
3. **공유 feature-detection 헬퍼 함수(또는 별도 `browserApi.js` 유틸
   모듈)로 추출** — `function supportsMatchMedia() {...}` 같은 걸
   `dashboard.js` 안에, 혹은 새 파일로 분리해 여러 호출부가 재사용하는
   형태.

## 이 코드베이스에 이미 있는 관례

`dashboard.js`에는 이미 정확히 이 클래스의 가드가 하나 존재한다 —
파일 하단 `:658`의 `if (typeof window !== "undefined") { ... }`
(브라우저 전용 auto-init 블록을 감싸는 용도, 이 파일의 주석이 직접
"Browser-only auto-init. Guarded so this file can be `require()`d
under Node ... without a real DOM/fetch"라고 설명한다). 이 파일은
지금까지 이 가드 하나를 인라인 `typeof` 체크로 처리해 왔고, 별도
유틸 모듈이나 헬퍼 함수로 추출한 적이 없다 — 파일 전체가 "가드가
필요하면 그 자리에서 `typeof` 체크"라는 로컬 관례를 이미 확립하고
있다.

## 채택 판단

**패턴 1(호출부 인라인)을 채택.** 근거:

- survey §1 스파이크가 이미 이 형태로 실측 green을 증명했다 — 추가
  검증 없이 바로 phase 2에 적용 가능한 정확한 diff가 있다.
- 이슈 자체가 F1을 "production 크래시 위험"으로 프레이밍한다
  (issue-36 conformance-review F1: "reachable in a default scenario
  for any user agent lacking `matchMedia`" — 다만 같은 문서가 "모든
  실제 배포 브라우저는 matchMedia를 지원해서 Blocking은 아니다"라고도
  적어 둠). 패턴 2(하네스 스텁만)는 테스트만 통과시키고 실제 프로덕션
  호출부는 여전히 무가드로 남긴다 — `matchMedia`가 없는 실제 UA(구형
  webview, 임베디드 브라우저 등)나 이 렌더 로직이 장차 비-브라우저
  컨텍스트에서 재사용될 경우(SSR 등, 현재는 없지만) 크래시가 그대로
  재현된다. 패턴 1은 이 두 경우 모두를 닫는다.
- 패턴 2는 패턴 1이 채택되면 기술적으로 불필요하다 — 스파이크가
  하네스 변경 없이 기존 테스트 파일 그대로 9/9 green을 만들었다.

패턴 3(공유 헬퍼/유틸 모듈)은 **reject** — proposal Rationale에서
구체 사유를 다룬다(요약: 현재 `matchMedia` 호출부가 파일 전체에 단
1곳뿐이라 추상화할 두 번째 호출자가 없고, 이 파일의 기존 관례(`:658`)도
인라인 `typeof` 체크이지 헬퍼 추출이 아니다 — "새 의존성·새 토큰 금지"
제약의 정신과도 맞지 않는 선제적 추상화).

## Sources

- https://developer.mozilla.org/en-US/docs/Web/API/Window/matchMedia
- https://developer.mozilla.org/en-US/docs/Learn_web_development/Extensions/Testing/Feature_detection
- https://github.com/ant-design/ant-design/issues/21096 (jsdom
  `matchMedia` 미구현이 여러 UI 라이브러리에서 반복적으로 부딪히는
  잘 알려진 하네스 공백이라는 근거)
- https://jestjs.io/docs/manual-mocks (Jest 생태계의 표준 `matchMedia`
  스텁 패턴 — 채택하지 않은 패턴 2의 실제 형태 참고용)
