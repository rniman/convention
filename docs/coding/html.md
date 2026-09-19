# HTML 기본 컨벤션

[코딩 목차](index.md) · 관련: [적용 기준](../baseline.md), [Material Forge 참고 기록](../projects/material-forge.md), [변경 검증](../quality/verification.md)

상태: **초안** · 작성일: 2026-09-19 · 적용 범위: 브라우저용 HTML 문서와 UI 마크업. JSX 차이는 별도 절에서 다룬다. XHTML·이메일 HTML은 제외한다.

문서 구조와 입력 요소의 의미를 명확히 하고, 작은 브라우저 도구에서도 키보드로 조작할 수 있게 한다. 아래 필수·권장·선택은 **채택 시 제안 강도**이며 현재 채택된 규칙이 아니다. CSS·JavaScript 전체 스타일, 프레임워크·빌드 도구 선정은 범위 밖이다.

## 문서 골격

| 항목 | 제안 | 강도 |
| --- | --- | --- |
| 문서 선언 | 첫 줄에 `<!DOCTYPE html>` 작성 | 필수 |
| 기본 구조 | `html`, `head`, `body`와 닫는 태그 명시 | 필수 |
| 언어 | `html`의 `lang`을 실제 주된 UI 언어에 맞춤 | 필수 |
| 문자 인코딩 | UTF-8로 저장하고 `head` 시작에 `<meta charset="utf-8">` 배치 | 필수 |
| 화면 크기 | `width=device-width, initial-scale=1.0` viewport 지정, 사용자 확대 제한 금지 | 권장 |
| 제목 | 문서 목적을 알 수 있는 `title` 작성 | 필수 |

`lang="ko"`는 한국어 UI 예시다. 영어 UI에는 `en`을 사용한다. 제목·문자 인코딩·viewport를 먼저 모아 문서 설정을 쉽게 찾는다. 문자 인코딩 선언은 문서 첫 1024바이트 안에 완전히 포함한다. 골격·메타데이터의 근거는 [HTML 문서 문법](https://html.spec.whatwg.org/multipage/syntax.html#writing-html-documents)과 [문서 메타데이터](https://html.spec.whatwg.org/multipage/semantics.html#the-meta-element)다.

```html
<!DOCTYPE html>
<html lang="ko">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>텍스처 도구</title>
  </head>
  <body>
    <main>
      <h1>텍스처 도구</h1>
      <label for="texture-name">텍스처 이름</label>
      <input id="texture-name" name="texture-name" type="text">
    </main>
  </body>
</html>
```

## 포맷과 명명

| 항목 | 제안 | 강도 |
| --- | --- | --- |
| 들여쓰기 | HTML·JSX 마크업은 단계마다 공백 2칸 | 권장 |
| 저장 형식 | UTF-8(BOM 없음), LF, 파일 끝 개행, 불필요한 줄 끝 공백 제거 | 필수 |
| 태그·속성 | HTML 태그·속성 이름은 소문자, 문자열 속성값은 큰따옴표 사용 | 필수 |
| 닫는 태그 | 일반 요소는 생략 가능한 경우에도 명시. `input`, `meta`, `img` 등 void 요소는 닫는 태그와 `/` 없이 작성 | 필수 |
| 줄바꿈 | 중첩 구조를 펼치고 긴 시작 태그는 속성별로 줄바꿈. 짧은 텍스트 요소는 한 줄 허용 | 권장 |
| 이름 | 새 파일·디렉터리와 직접 정하는 `id`, `class`, `data-*` 이름은 의미 있는 영문 소문자 `kebab-case` | 권장 |
| 식별자 | `id`는 문서 안에서 유일하게 유지. 반복 스타일에는 `class` 사용 | 필수 |
| 주석 | 구획·예외 이유를 `<!-- ... -->`로 기록하고 코드 자체를 반복 설명하지 않음 | 권장 |

공백 2칸은 참고 코드의 일부 배치를 바탕으로 한 새 제안이며 일관된 기존 합의로 단정하지 않는다. [C++ 포맷](cpp/formatting.md)의 탭 4칸은 C++ 범위에 유지한다. HTML 표준은 이 들여쓰기·명명·따옴표 스타일을 강제하지 않으며, 여기서는 변경 내용을 읽기 쉽게 하려는 개인안이다. 줄 길이의 수치 제한은 미결정이다.

`pre`·`textarea`의 텍스트나 인라인 요소 사이 공백처럼 출력에 영향을 주는 부분은 기계적으로 재배치하지 않는다. SVG의 `viewBox` 등 다른 문법과 외부 API가 정한 이름은 원래 표기를 따른다. 기존 공개 경로·저장 키·연동 식별자는 호환성 검토 없이 바꾸지 않는다. 생성물·외부 코드는 원본 도구의 포맷을 유지할 수 있다.

HTML 불리언 속성은 참일 때 `disabled`처럼 쓰고 거짓일 때 제거한다(필수). `disabled="false"`도 비활성화이므로 사용하지 않는다. `aria-expanded="false"` 같은 ARIA 상태는 이 생략 규칙을 적용하지 않는다. 문법 근거: [속성](https://html.spec.whatwg.org/multipage/syntax.html#attributes-2), [불리언 속성](https://html.spec.whatwg.org/multipage/common-microsyntaxes.html#boolean-attributes).

## 의미 있는 구조와 조작 요소

- **필수:** 동작은 `button`, 이동은 `a`와 유효한 `href`, 입력은 목적에 맞는 `input`·`select`·`textarea`로 표현한다. 클릭 가능한 `div`를 기본 선택으로 사용하지 않는다.
- **필수:** 제출용이 아닌 버튼에는 `type="button"`을 지정한다. 폼 제출에는 `type="submit"`을 명시해 의도하지 않은 제출을 막는다.
- **권장:** 주 콘텐츠에는 `main`, 제목에는 순서에 맞는 `h1`~`h6`, 항목 목록에는 `ul`·`ol`을 사용한다. 제목 크기를 이유로 제목 단계를 고르지 않는다. 의미 없는 배치 묶음에는 `div`를 사용해도 된다.
- **권장:** 단순 접기 UI는 `details`·`summary`를 우선 검토한다. 직접 구현할 때는 버튼의 `aria-expanded`와 실제 표시 상태를 일치시킨다.
- **필수:** 키보드로 모든 조작에 접근할 수 있게 하고 포커스를 식별할 수 있게 한다. 대체 표시 없이 `outline: none`을 적용하지 않는다. 특수 위젯은 키보드 동작·포커스·상태 전달을 별도로 구현·검증한다.

기본 요소는 의미와 기본 조작을 함께 제공한다. 이는 [HTML 폼 요소](https://html.spec.whatwg.org/multipage/forms.html), [WCAG 2.2 키보드](https://www.w3.org/WAI/WCAG22/Understanding/keyboard.html), [포커스 표시](https://www.w3.org/WAI/WCAG22/Understanding/focus-visible.html)를 바탕으로 한 제안이며 WCAG 전체 준수를 보장하는 목록은 아니다.

## 입력·이미지·미리보기

- **필수:** 입력에는 보이는 레이블을 연결한다. `label for`와 입력의 `id`를 맞추거나 `label` 안에 입력을 넣는다. `placeholder`·인접한 `div` 텍스트만으로 대체하지 않는다. 화면에 레이블을 둘 수 없는 예외는 `aria-label` 등 접근 가능한 이름과 이유를 명시한다. [WAI 레이블 안내](https://www.w3.org/WAI/tutorials/forms/labels/)
- **권장:** 관련 입력 묶음은 `fieldset`·`legend`로 설명하고, 값 범위·단위·오류를 텍스트로 안내한다. 숫자 입력의 `min`·`max`·`step`은 의도에 맞게 지정하되 실제 처리 시의 값 검증을 대체하지 않는다.
- **필수:** 의미 있는 `img`에는 목적에 맞는 `alt`, 장식용에는 `alt=""`를 지정한다. `canvas` 결과에는 설명·대체 콘텐츠를 제공하고, 생성 조건·결과 크기 같은 핵심 정보는 주변 텍스트로도 제공한다.
- **권장:** 긴 작업의 진행·완료·실패를 텍스트로 구분하고 필요한 상태 알림에 `role="status"` 등을 사용한다. 잦은 중간 갱신을 모두 읽게 만들지 않는다.

다음은 레이블·도움말 연결 예시이며 생성 동작을 구현한 코드는 아니다.

```html
<label for="output-size">출력 크기</label>
<select
  id="output-size"
  name="output-size"
  aria-describedby="output-size-help"
>
  <option value="512">512 × 512</option>
  <option value="1024">1024 × 1024</option>
</select>
<p id="output-size-help">저장할 이미지의 픽셀 크기입니다.</p>
<button type="button">미리보기 생성</button>
```

## CSS·스크립트와 배포 경계

HTML 구조, CSS 표현, JavaScript 동작은 역할별로 구분한다(권장). 단일 HTML 배포가 필요한 경우 `style`·`script` 내장을 허용한다(선택). 배포 파일이 하나라는 이유만으로 소스도 반드시 한 파일이어야 하는 것은 아니다. 외부 파일 분리·번들러 도입은 프로젝트 제약에 따라 결정한다.

일반 HTML에서는 이벤트 속성에 JavaScript 문자열을 넣기보다 `addEventListener`로 동작을 연결한다(권장). 외부 classic script의 `defer`는 파싱 후 문서 순서대로 실행할 때 사용하고, 의존 순서가 있는 스크립트에 `async`를 일괄 적용하지 않는다. 인라인 classic script에 `defer`를 붙여 실행 시점을 늦출 수는 없다. `type="module"`과 일반 script의 실행 조건은 구분한다. [HTML script 처리 기준](https://html.spec.whatwg.org/multipage/scripting.html#the-script-element)

외부 라이브러리는 버전과 네트워크 의존성을 기록한다(권장). 단일 파일과 오프라인 실행은 별개이며, 오프라인 지원 여부는 실제 실행 결과로 판단한다. 사용자 입력을 표시할 때는 HTML 문자열 삽입보다 `textContent`나 프레임워크의 기본 텍스트 렌더링을 사용한다(권장). HTML 삽입이 필요한 예외에는 신뢰 경계와 정제 방식을 별도로 정한다.

## React JSX와의 차이

JSX를 HTML 문법 검사만으로 판정하지 않는다. 아래는 React 공식 가이드에 따른 구문 차이이며 HTML 기본 스타일의 예외다. [Writing Markup with JSX](https://react.dev/learn/writing-markup-with-jsx)

| 일반 HTML | React JSX |
| --- | --- |
| `class="preview-panel"` | `className="preview-panel"` |
| `for="seed"` | `htmlFor="seed"` |
| `<input type="number">` | `<input type="number" />` |
| `disabled` / 속성 제거 | `disabled={isBusy}` |
| JavaScript에서 이벤트 등록 | `onClick={handleGenerate}` |
| 문자열 `style` 속성 | `style={{ width: previewSize }}` 같은 객체 |

JSX 컴포넌트는 `SeedInput`처럼 대문자로 시작한다. `aria-*`·`data-*`는 하이픈 표기를 유지한다. React 상태가 관리하는 입력은 상태 갱신도 함께 구현하며, 이 문서는 Hooks·상태 관리 규약까지 정하지 않는다. JSX 변환기나 개발용 실행 방식은 HTML 표준 기능이 아니므로 프로젝트에서 별도로 선택한다.

## 검증과 미결정 사항

변경한 HTML의 중첩·중복 `id`·레이블 연결을 확인한다(필수). UI 변경 시 브라우저의 콘솔 오류, Tab 이동·버튼·입력 조작, 포커스, 좁은 창과 확대 상태를 확인한다(필수). HTML 검사와 JSX 변환 검사는 구분하고, 실행하지 않은 검증은 코드 검토로 표시한다. 자세한 결과 기록은 [변경 검증](../quality/verification.md)을 따른다.

- **미결정:** 공통 채택 여부, 들여쓰기 최종 선택, 줄 길이 수치, 지원 브라우저·버전, 자동 검사·포맷 도구, CSS·JavaScript 상세 규칙.
- **보류·폐기:** 이번 작성에서 확정한 항목 없음.
- **예외:** 기존 프로젝트의 배포 제약·프레임워크 문법은 적용 범위와 이유를 프로젝트 문서에 남긴다.

## 근거와 변경 기록

외부 근거 확인일: **2026-09-19**. HTML 근거는 WHATWG **HTML Living Standard**(확인 페이지 최종 갱신 2026-09-17), 접근성은 **WCAG 2.2** 해설과 WAI Forms Tutorial, JSX는 React 공식 현행 가이드다. Living Standard와 React 가이드는 고정 판본이 아니며 특정 브라우저·React 최소 버전을 이 문서에서 확정하지 않는다. 이미지·캔버스 의미는 [HTML img](https://html.spec.whatwg.org/multipage/embedded-content.html#the-img-element)·[canvas](https://html.spec.whatwg.org/multipage/canvas.html#the-canvas-element)를 참고한다.

로컬 코드·문서의 확인 범위와 차이는 [Material Forge 참고 기록](../projects/material-forge.md)에 둔다. `ref/`의 기존 C++·Git 자료에서는 HTML 전용 채택 근거를 찾지 못했다. 표준의 허용 문법과 개인 스타일 제안은 구분하며 새 공통 채택은 하지 않았다.

- 2026-09-19: 참고 프로젝트의 문서 골격·JSX UI와 개선 기록을 바탕으로 최초 초안을 작성했다. 표준 문법, 개인 포맷 제안, 프로젝트 제약을 구분했다.
