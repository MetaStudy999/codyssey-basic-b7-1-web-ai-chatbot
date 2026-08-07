# B7-1 Independent Review Contract

## Source of Truth
1. `b7-1-mission.pdf`
2. `b7-1-mission.md`
3. 공식 Evaluation (현재 G1에서 MISSING으로 판정; 새로 발견되면 재대조)
4. `MISSION-WORK-PACKET.md`

## Review scope
BLOCKER와 MAJOR만 보고한다.
- Mission 필수 요구 누락
- 테스트 실패
- auth 우회 또는 다른 사용자 로그 노출
- AI key/credential 노출
- timeout/error handling 누락
- 문서와 코드의 명백한 모순
- 실제 실행하지 않은 항목을 PASS라고 주장한 경우

## Do not
- 대규모 재설계/리팩터링
- Source 밖 기능 추가
- 스타일 선호만으로 수정
- Human runtime을 자동 테스트로 PASS 처리

## Tests
```bash
pytest -q
```

## Status
`TODO / IMPLEMENTED / TESTED / PASS / NEEDS-RUNTIME / BLOCKED`

## Stop
BLOCKER=0, MAJOR=0이면 독립 리뷰를 종료한다. 외부 URL, 실제 AI credential, 팀별 10+ commit evidence는 Human runtime/evidence로 남겨 둔다.
