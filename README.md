# ReaDream API

## chat
꿈 내용을 입력하면 해석해주는 기능

## [POST] chat
- **request** 유저의 꿈 내용 (type: json)
- **response** 유저의 꿈 해석내용 (type: xml 형식의 String)
```
{domain}/chat
```

### Reequest
#### header
| key          | value                           |
|--------------|---------------------------------|
| Content-Type | application/json; charset=UTF-8 |

#### body
| parameter      | type   | required | description   |
|----------------|--------|----------|---------------|
| requestContent | String | True     | dream content |

#### body example
```json
{
    "requestContent": "집에 가는 길에 동전을 줍는 꿈을 꿨어."
}
```

### Response
#### example
```
" <Response>\n  <Title>행운의 기회</Title>\n  <Interpret>꿈에서 집에 가는 길에 동전을 줍는 것은 뜻밖의 행운과 기회가 찾아올 것이라는 길조입니다. 마음의 준비를 하고 그 기회를 잡아보세요. 열정을 가지고 임한다면 좋은 결과를 얻을 수 있을 것입니다.</Interpret>\n  <Score>4</Score>\n  <Summary>The dreamer picks up coins while going home, indicating unexpected good luck and opportunities.</Summary>\n</Response>"
```

| tag       | type   | description       |
|-----------|--------|-------------------|
| Response  |        |                   |
| Title     | String |                   |
| Interpret | String |                   |
| Score     | Int    | lucky score (1~5) |
| Summary   | String | for illustration  |



## chat
꿈 내용을 바탕으로 그림을 그려주는 기능

## [POST] chat
- **request** 유저의 꿈 요약내용(Summary) 및 행운점수(Score) (type: json)
- **response** 유저의 꿈 생성 이미지 (type: 이미지 url String)
```
{domain}/illustrate
```

### Reequest
#### header
| key          | value                           |
|--------------|---------------------------------|
| Content-Type | application/json; charset=UTF-8 |

#### body
| parameter      | type   | required | description   |
|----------------|--------|----------|---------------|
| requestContent | String | True     | dream content |

#### body example
```json
{
    "situation": "The dreamer picks up coins while going home, indicating unexpected good luck and opportunities.",
    "score": 4
}
```

### Response
#### example
```
"https://mblogthumb-phinf.pstatic.net/MjAyMDA2MDFfNzQg/MDAxNTkwOTkzODU4MTg1.MbMtqBLDTWrZabpkQs3UQtXwtyTBL2PD3Hf9ndaP72sg.5YUAeus3aYY3GjhF6vIQimSAXulR1UalevOWPaF4tVcg.PNG.leekywood/0001.png?type=w420"
```

| key | type   | description       |
|-----|--------|-------------------|
|     | String | image url         |

- 주의: 한번 생성된 이미지 url을 통해 이미지 데이터를 받아올 수 있는 기한은 약 5~10분 남짓
- 기한 내에는 여러번 조회 가능
- 이미지 하나 생성할 때마다 $0.04 ㅠㅠ


