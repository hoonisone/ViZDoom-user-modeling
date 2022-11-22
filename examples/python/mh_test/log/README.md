log data 형식

<log>: List<step_state>
<step_state>: {<objects>, <labels>}
<objects>: [<object>]
<labels>: [<label>]
<object>: 게임 내 객체 정보 (id, name, 위치, 속도, 각도) 
<labels>: 플레이어 화면 내 객체 object detection 수행 결과인 한 오브젝트의 정보 (id, bounding box) 