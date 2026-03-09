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
    {"id": 11, "text": "気が進まないことは理由をつけて後回しにしてしまうことがある", "type": "AC"},
    {"id": 12, "text": "責任感を大切にしている", "type": "CP"},
    {"id": 13, "text": "人の面倒を見ることが多い", "type": "NP"},
    {"id": 14, "text": "物事の原因や仕組みを考えることが多い", "type": "A"},
    {"id": 15, "text": "「わぁ」「へぇ」など驚きの言葉をよく口にする", "type": "FC"},
    {"id": 16, "text": "相手の表情や様子を気にすることがある", "type": "AC"},
    {"id": 17, "text": "物事を正確に判断できるほうだ", "type": "A"},
    {"id": 18, "text": "身近な人の帰りが遅いと心配になる", "type": "NP"},
    {"id": 19, "text": "思っていることをあまり口に出さないタイプだ", "type": "AC"},
    {"id": 20, "text": "じっと静かにしているのが苦手だ", "type": "FC"},
    {"id": 21, "text": "さまざまな情報や事実を集めて考えることが多い", "type": "A"},
    {"id": 22, "text": "自分の希望をはっきり主張することがある", "type": "FC"},
    {"id": 23, "text": "「〜すべきだ」といった言い方をすることがある", "type": "CP"},
    {"id": 24, "text": "人との付き合い方が比較的うまい", "type": "AC"},
    {"id": 25, "text": "相手のミスや欠点に厳しくなることがある", "type": "CP"},
    {"id": 26, "text": "周囲の目をあまり気にしない", "type": "FC"},
    {"id": 27, "text": "相手が喜んでくれるよう努力することが多い", "type": "AC"},
    {"id": 28, "text": "「すみません」「ごめんなさい」と言うことが多い", "type": "AC"},
    {"id": 29, "text": "感情に流されず判断しようとする", "type": "A"},
    {"id": 30, "text": "新しいことに興味を持ちやすい", "type": "FC"},
    {"id": 31, "text": "理想を大切にして行動したいと思う", "type": "CP"},
    {"id": 32, "text": "行動する前にしっかり計画を立てる", "type": "A"},
    {"id": 33, "text": "会話ではできるだけ感情的にならないようにしている", "type": "A"},
    {"id": 34, "text": "困っている人を見ると慰めたり声をかけたりする", "type": "NP"},
    {"id": 35, "text": "ボランティアなどで積極的に動くことがある", "type": "NP"},
    {"id": 36, "text": "自分の意見をはっきりと主張する", "type": "CP"},
    {"id": 37, "text": "理屈より直感で判断することがある", "type": "FC"},
    {"id": 38, "text": "状況に応じて柔軟に対応できる", "type": "NP"},
    {"id": 39, "text": "欲しいものははっきり求めるほうだ", "type": "FC"},
    {"id": 40, "text": "相手の失敗を受け入れて許すことができる", "type": "NP"},
    {"id": 41, "text": "誰とでも比較的よく会話する", "type": "A"},
    {"id": 42, "text": "頼まれると断れないことが多い", "type": "NP"},
    {"id": 43, "text": "道徳や倫理を大切にしている", "type": "CP"},
    {"id": 44, "text": "人にはできるだけ温かく接したいと思っている", "type": "NP"},
    {"id": 45, "text": "不満や文句を感じることが多い", "type": "AC"},
    {"id": 46, "text": "自分の考えを言うまでに少し時間がかかることがある", "type": "AC"},
    {"id": 47, "text": "相手の目を見て姿勢を正して話すほうだ", "type": "A"},
    {"id": 48, "text": "嬉しいときは素直に喜びを表現する", "type": "FC"},
    {"id": 49, "text": "ルールや規則はきちんと守るべきだと思う", "type": "CP"},
    {"id": 50, "text": "行動する前に計画を見直しながら進めるほうだ", "type": "A"},
]

type_labels = {
    "CP": "CP（厳しさ・規範性）",
    "NP": "NP（優しさ・養育性）",
    "A": "A（冷静さ・合理性）",
    "FC": "FC（自由さ・感情表現）",
    "AC": "AC（順応性・気づかい）"
}

type_comments = {
    "CP": "正しさや責任感を大切にし、筋を通そうとする傾向があります。強みは信頼感ですが、行きすぎると自分にも他人にも厳しくなりやすい面があります。",
    "NP": "思いやりや共感力が高く、人を支える力が強い傾向があります。強みは優しさですが、相手を優先しすぎて自分を後回しにしやすい面があります。",
    "A": "落ち着いて状況を見て、合理的に判断する力が高い傾向があります。強みは分析力ですが、感情表現が少なく見えることもあります。",
    "FC": "自由さや好奇心、感情の豊かさが強みとして表れやすい傾向があります。魅力はのびのびした表現力ですが、勢いで動きすぎることもあります。",
    "AC": "相手に配慮し、場に合わせる力が高い傾向があります。強みは協調性ですが、我慢しすぎたり本音を抑えたりしやすい面があります。"
}

html = """
<!doctype html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <title>エゴグラム診断</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
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
        h1, h2 {
            color: #444;
        }
        .lead {
            background: #f8f7fc;
            padding: 16px;
            border-radius: 12px;
            margin-bottom: 24px;
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
        button:hover {
            opacity: 0.92;
        }
        .result-box {
            margin-top: 36px;
            padding: 20px;
            border-radius: 14px;
            background: #f7f4ff;
            border: 1px solid #ddd;
        }
        .scores {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
            gap: 10px;
            margin: 16px 0 20px;
        }
        .score-card {
            background: white;
            border: 1px solid #ddd;
            border-radius: 12px;
            padding: 12px;
        }
        .note {
            font-size: 14px;
            color: #666;
        }
        canvas {
            margin-top: 24px;
            background: white;
            border-radius: 12px;
            padding: 12px;
        }
    </style>
</head>
<body>
    <h1>エゴグラム診断</h1>

    <div class="lead">
        <p>各項目について、もっとも近いものを選んでください。</p>
        <p>採点ルール：<strong>はい = 2点 / どちらとも言えない = 1点 / いいえ = 0点</strong></p>
        <p class="note">※これは医療診断ではなく、自己理解のためのセルフチェックです。</p>
    </div>

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

        <div class="scores">
            <div class="score-card"><strong>CP</strong><br>{{ scores["CP"] }} 点</div>
            <div class="score-card"><strong>NP</strong><br>{{ scores["NP"] }} 点</div>
            <div class="score-card"><strong>A</strong><br>{{ scores["A"] }} 点</div>
            <div class="score-card"><strong>FC</strong><br>{{ scores["FC"] }} 点</div>
            <div class="score-card"><strong>AC</strong><br>{{ scores["AC"] }} 点</div>
        </div>

        <canvas id="egoChart" width="400" height="220"></canvas>

        <p class="note">点数の高低に良し悪しはありません。自分の傾向のバランスを見るための目安として使ってください。</p>
    </div>

    <script>
        const ctx = document.getElementById('egoChart').getContext('2d');
        new Chart(ctx, {
            type: 'bar',
            data: {
                labels: ['CP', 'NP', 'A', 'FC', 'AC'],
                datasets: [{
                    label: '点数',
                    data: [{{ scores["CP"] }}, {{ scores["NP"] }}, {{ scores["A"] }}, {{ scores["FC"] }}, {{ scores["AC"] }}]
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: { display: false }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        suggestedMax: 20,
                        ticks: {
                            stepSize: 2
                        }
                    }
                }
            }
        });
    </script>
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

if __name__ == "__main__":
    app.run(debug=True)