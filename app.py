from flask import Flask, request, render_template_string

app = Flask(__name__)

questions = [
    {"id": 1, "text": "行動が素早く、効率よく物事を進めるほうだ", "type": "A"},
    {"id": 2, "text": "思ったことを率直に表現する、自由な雰囲気がある", "type": "FC"},
    {"id": 3, "text": "周囲の人と歩調を合わせて行動することが多い", "type": "AC"},
    {"id": 4, "text": "相手の良いところを見つけて褒めることが多い", "type": "NP"},
    {"id": 5, "text": "昔からの習慣や伝統を大切にしている", "type": "CP"},
    {"id": 6, "text": "感じたことが表情に出やすい", "type": "FC"},
    {"id": 7, "text": "相手の話を聞くと自然に共感することが多い", "type": "NP"},
    {"id": 8, "text": "物事を現実的に見て判断するほうだ", "type": "A"},
    {"id": 9, "text": "遠慮がちで控えめな性格だ", "type": "AC"},
    {"id": 10, "text": "物事を批判的な視点で考えることがある", "type": "CP"},
]

type_labels = {
    "CP": "CP（厳しさ・規範性）",
    "NP": "NP（優しさ・養育性）",
    "A": "A（冷静さ・合理性）",
    "FC": "FC（自由さ・感情表現）",
    "AC": "AC（順応性・気づかい）"
}

type_comments = {
    "CP": "正しさや責任感を大切にし、筋を通そうとする傾向があります。",
    "NP": "思いやりや共感力が高く、人を支える力が強い傾向があります。",
    "A": "落ち着いて状況を見て、合理的に判断する力が高い傾向があります。",
    "FC": "自由さや好奇心、感情の豊かさが強みとして表れやすい傾向があります。",
    "AC": "相手に配慮し、場に合わせる力が高い傾向があります。"
}

html = """
<!doctype html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <title>エゴグラム診断</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Hiragino Sans", "Yu Gothic", sans-serif;
            max-width: 920px;
            margin: 0 auto;
            padding: 24px 16px 60px;
            color: #333;
            line-height: 1.7;
            background: #fff;
        }
        .question {
            border: 1px solid #e3e3e3;
            border-radius: 12px;
            padding: 16px;
            margin-bottom: 14px;
            background: #fafafa;
        }
        .question-title {
            font-weight: bold;
            margin-bottom: 10px;
        }
        .choices label {
            display: block;
            margin: 6px 0;
            cursor: pointer;
        }
        button {
            background: #6b5b95;
            color: white;
            border: none;
            border-radius: 10px;
            padding: 14px 24px;
            font-size: 16px;
            cursor: pointer;
            margin-top: 12px;
        }
        .result-box {
            margin-top: 36px;
            padding: 20px;
            border-radius: 14px;
            background: #f7f4ff;
            border: 1px solid #ddd;
        }
    </style>
</head>
<body>
    <h1>エゴグラム診断</h1>
    <p>各項目について、もっとも近いものを選んでください。</p>
    <p>採点ルール：はい = 2点 / どちらとも言えない = 1点 / いいえ = 0点</p>

    <form method="post">
        {% for q in questions %}
        <div class="question">
            <div class="question-title">Q{{ q.id }}. {{ q.text }}</div>
            <div class="choices">
                <label><input type="radio" name="q{{ q.id }}" value="2" required> はい</label>
                <label><input type="radio" name="q{{ q.id }}" value="1"> どちらとも言えない</label>
                <label><input type="radio" name="q{{ q.id }}" value="0"> いいえ</label>
            </div>
        </div>
        {% endfor %}
        <button type="submit">結果を見る</button>
    </form>

    {% if scores %}
    <div class="result-box">
        <h2>診断結果</h2>
        <p><strong>もっとも高かったタイプ：</strong>{{ highest_label }}</p>
        <p>{{ highest_comment }}</p>
        <ul>
            <li>CP: {{ scores["CP"] }} 点</li>
            <li>NP: {{ scores["NP"] }} 点</li>
            <li>A: {{ scores["A"] }} 点</li>
            <li>FC: {{ scores["FC"] }} 点</li>
            <li>AC: {{ scores["AC"] }} 点</li>
        </ul>
    </div>
    {% endif %}
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    scores = None
    highest_label = None
    highest_comment = None

    if request.method == "POST":
        scores = {"CP": 0, "NP": 0, "A": 0, "FC": 0, "AC": 0}

        for q in questions:
            answer = int(request.form.get(f"q{q['id']}", 0))
            scores[q["type"]] += answer

        highest_type = max(scores, key=scores.get)
        highest_label = type_labels[highest_type]
        highest_comment = type_comments[highest_type]

    return render_template_string(
        html,
        questions=questions,
        scores=scores,
        highest_label=highest_label,
        highest_comment=highest_comment
    )