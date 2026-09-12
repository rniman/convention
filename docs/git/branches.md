# Git 브랜치 명명 규칙

[Git·협업 목차](index.md) · 관련: [커밋 메시지](commit-messages.md)

상태: 채택 · 적용 범위: 개인 작업 브랜치 이름 · Git의 유효한 ref 이름 안에서 적용

브랜치 이름은 작업의 목적을 짧게 식별한다. 생성 기준 브랜치와 병합 방법은 별도 작업 흐름에서 정한다.

## 형식

```text
<type>/<short-description>
<type>/<issue-number>-<short-description>
```

- **필수:** 작업 이름은 영어 소문자·숫자와 단어 구분용 `-`를 사용한다. type과 설명 사이는 `/` 하나로 구분한다.
- **권장:** 설명은 2~4단어를 기준으로 작성하되 의미를 보존하려면 더 길게 쓸 수 있다. `work`, `update`, `temp`만으로 끝내지 않는다.
- **선택:** 실제 관련 이슈가 있으면 설명 앞에 번호를 넣는다. `#`는 붙이지 않으며 번호를 만들어 넣지 않는다.
- **필수:** 설명의 시작·끝이나 연속 위치에 `-`를 두지 않는다. 공백·밑줄·추가 `/`는 사용하지 않는다.
- 커밋 메시지를 한국어로 작성해도 브랜치 이름은 영어로 유지한다.

## type

| type | 용도 | 예시 |
| --- | --- | --- |
| `feature/` | 새 기능 작업 | `feature/player-dash` |
| `fix/` | 일반 버그 수정 | `fix/23-boss-health-bar` |
| `refactor/` | 구조 개선 | `refactor/input-handler` |
| `hotfix/` | 배포된 버전의 긴급 수정 | `hotfix/save-load-crash` |
| `release/` | 릴리스 준비 | `release/v1.2.0` |
| `docs/` | 문서 작업 | `docs/commit-convention` |
| `test/` | 테스트·실험 | `test/lighting-model` |
| `chore/` | 빌드·CI 등을 포함한 유지보수 | `chore/update-build-config` |

기존 자료의 `bugfix/`는 사용자가 제공한 최신 방식인 `fix/`로 통일한다. `chore/`는 기존 자료의 유지보수 분류를 유지한다. 별도 성능 브랜치 접두어를 추가하지 않고, 동작을 유지하는 성능 작업은 `refactor/`를 기본으로 하되 실제 기능 추가·오류 수정이면 그 목적을 따른다.

브랜치 type은 작업 전체의 목적이며 각 커밋의 type과 일대일로 맞출 필요가 없다. 예를 들어 `feature/player-dash`에는 `feat`, `test`, `fix` 커밋이 함께 들어갈 수 있다. `test/`의 실험 구현도 커밋에서는 실제 변경 내용에 맞춰 분류한다.

## 릴리스·장기 브랜치 예외

`release/`는 짧은 설명 대신 프로젝트에서 확정한 버전 식별자를 사용한다. `release/v1.2.0`처럼 버전 구분용 점을 허용하며 2~4단어 권장을 적용하지 않는다. 아직 정하지 않은 릴리스 번호를 추측하지 않는다.

`main`, `develop` 등 장기 브랜치는 작업 이름 형식에서 제외한다. 이 문서가 `develop`이나 Git Flow 도입을 요구하지는 않는다. `hotfix/`, `release/`를 어디서 분기하고 어디에 병합할지는 프로젝트의 배포 흐름에서 결정한다.

## 이름 검증

Git 문법의 유효성은 다음 명령으로 확인할 수 있다. 이 명령은 브랜치를 생성하지 않으며 위 개인 명명 정책까지 검사하지 않는다.

```shell
git check-ref-format --branch fix/23-boss-health-bar
```

Git은 개인 규칙보다 넓은 이름을 허용한다. 소문자·kebab-case·type 목록은 도구의 강제 규칙이 아닌 개인 선택이다. 기존 같은 이름이나 상위 ref와의 충돌 여부는 실제 생성 시 별도로 확인한다.

## 근거와 출처

사용자 제공안과 [기존 Git 자료](../../ref/DevRnimanConvention/Git_Commit_Convention_Kor.md)의 구조를 유지했다. `feature/`와 커밋의 `feat`는 기존 선호대로 구분한다. 릴리스 버전의 점 표기 예외, 브랜치와 개별 커밋의 목적 구분을 명시했다.

- [Git — git-check-ref-format](https://git-scm.com/docs/git-check-ref-format)

출처 확인일: 2026-09-12. 병합 전략·브랜치 수명·릴리스 버전 체계는 후속 정리 대상이다.

채택일: 2026-09-12. 명시된 적용 범위 안에서 채택하며, 후속 정리 대상은 제외한다.
