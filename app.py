import random
from flask import Flask, request, render_template_string

app = Flask(__name__)

QUESTIONS = [
    {"id": 1, "text": "ルールや約束はきちんと守るべきだと思う", "type": "CP"},
    {"id": 2, "text": "自分にも他人にも厳しいほうだ", "type": "CP"},
    {"id": 3, "text": "怠けている人を見ると気になる", "type": "CP"},
    {"id": 4, "text": "責任感が強いと言われる", "type": "CP"},
    {"id": 5, "text": "筋を通さない態度が苦手だ", "type": "CP"},
    {"id": 6, "text": "きちんとしていないと落ち着かない", "type": "CP"},
    {"id": 7, "text": "物事の善悪をはっきりさせたい", "type": "CP"},
    {"id": 8, "text": "人のだらしなさが気になる", "type": "CP"},
    {"id": 9, "text": "自分を甘やかすのが苦手だ", "type": "CP"},
    {"id": 10, "text": "正しさを大事にするほうだ", "type": "CP"},

    {"id": 11, "text": "困っている人を助けたいと思う", "type": "NP"},
    {"id": 12, "text": "人の気持ちに共感しやすい", "type": "NP"},
    {"id": 13, "text": "相手を励ましたり支えたりすることが多い", "type": "NP"},
    {"id": 14, "text": "面倒見がよいほうだ", "type": "NP"},
    {"id": 15, "text": "人の成長を見守るのが好きだ", "type": "NP"},
    {"id": 16, "text": "優しく接することを大事にしている", "type": "NP"},
    {"id": 17, "text": "人の立場を考えて行動することが多い", "type": "NP"},
    {"id": 18, "text": "つい世話を焼いてしまう", "type": "NP"},
    {"id": 19, "text": "相手を受け入れようとするほうだ", "type": "NP"},
    {"id": 20, "text": "誰かの役に立てるとうれしい", "type": "NP"},

    {"id": 21, "text": "感情よりも事実を優先して考える", "type": "A"},
    {"id": 22, "text": "判断するときは情報を集めるほうだ", "type": "A"},
    {"id": 23, "text": "物事を冷静に分析するのが得意だ", "type": "A"},
    {"id": 24, "text": "衝動より合理性を重視する", "type": "A"},
    {"id": 25, "text": "感情的な議論は苦手だ", "type": "A"},
    {"id": 26, "text": "何かを決める前に比較検討する", "type": "A"},
    {"id": 27, "text": "データや根拠を重視する", "type": "A"},
    {"id": 28, "text": "客観的に考えようとすることが多い", "type": "A"},
    {"id": 29, "text": "損得や効率を考えるほうだ", "type": "A"},
    {"id": 30, "text": "一歩引いて全体を見ることができる", "type": "A"},

    {"id": 31, "text": "楽しいことや面白いことが好きだ", "type": "FC"},
    {"id": 32, "text": "思いついたらすぐ動きたくなる", "type": "FC"},
    {"id": 33, "text": "自分らしさを大事にしたい", "type": "FC"},
    {"id": 34, "text": "感情表現が豊かなほうだ", "type": "FC"},
    {"id": 35, "text": "ワクワクすることを優先したい", "type": "FC"},
    {"id": 36, "text": "好き嫌いが比較的はっきりしている", "type": "FC"},
    {"id": 37, "text": "自由でいたい気持ちが強い", "type": "FC"},
    {"id": 38, "text": "好奇心が強いほうだ", "type": "FC"},
    {"id": 39, "text": "場を明るくすることが多い", "type": "FC"},
    {"id": 40, "text": "やりたいことを我慢しすぎるとつらい", "type": "FC"},

    {"id": 41, "text": "人に嫌われないよう気をつかう", "type": "AC"},
    {"id": 42, "text": "自分より相手を優先しがちだ", "type": "AC"},
    {"id": 43, "text": "頼まれると断りにくい", "type": "AC"},
    {"id": 44, "text": "相手の顔色を見てしまうことが多い", "type": "AC"},
    {"id": 45, "text": "本音を言うのが苦手だ", "type": "AC"},
    {"id": 46, "text": "対立を避けようとするほうだ", "type": "AC"},
    {"id": 47, "text": "空気を読みすぎて疲れることがある", "type": "AC"},
    {"id": 48, "text": "自分の希望を後回しにしやすい", "type": "AC"},
    {"id": 49, "text": "周囲に合わせないと不安になることがある", "type": "AC"},
    {"id": 50, "text": "評価されるかどうかが気になりやすい", "type": "AC"},
]

TYPE_LABELS = {
    "CP": "CP（厳しさ・責任感）",
    "NP": "NP（やさしさ・養育性）",
    "A": "A（冷静さ・合理性）",
    "FC": "FC（自由さ・感情表現）",
    "AC": "AC（順応性・気づかい）",
}

TYPE_COMMENTS = {
    "CP": "責任感や倫理観が強く、きちんとした姿勢を大切にする傾向があります。反面、自分にも他人にも厳しくなりすぎると、しんどさにつながることがあります。",
    "NP": "思いやりや共感力が高く、人を支える力がある傾向があります。反面、世話を焼きすぎたり、自分を後回しにしすぎたりしやすい面もあります。",
    "A": "冷静に考え、客観的に判断する力が高い傾向があります。反面、感情表現が抑えられすぎると、距離感が出やすくなることがあります。",
    "FC": "自由さや好奇心、感情の豊かさが強みとして表れやすい傾向があります。反面、衝動性や気分優先になりすぎると不安定さにつながることがあります。",
    "AC": "周囲への配慮や適応力が高く、人間関係を円滑に保つ力があります。反面、合わせすぎて疲れたり、本音を抑え込みやすかったりすることがあります。",
}

INDEX_HTML = """
<!doctype html>
<html lang="ja">
<head>
  <meta charset="UTF-8">
  <title>エゴグラム50問チェック</title>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <style>
    body {
      font-family: sans-serif;
      max-width: 900px;
      margin: 40px auto;
      padding: 0 16px;
      color: #333;
      line-height: 1.7;
    }
    .question {
      border: 1px solid #ddd;
      border-radius: 10px;
      padding: 16px;
      margin-bottom: 16px;
      background: #fafafa;
    }
    .choices label {
      display: block;
      margin-bottom: 8px;
      cursor: pointer;
    }
    button {
      background: #6a5acd;
      color: white;
      border: none;
      padding: 12px 24px;
      border-radius: 8px;
      cursor: pointer;
      font-size: 16px;
    }
    .note {
      font-size: 14px;
      color: #666;
    }
  </style>
</head>
<body>
  <h1>エゴグラム 50問セルフチェック</h1>
  <p>各質問について、もっとも近いものを選んでください。</p>
  <p class="note">※これは医療診断ではなく、自己理解のためのセルフチェックです。</p>

  <form method="post" action="/result">
    {% for q in questions %}
      <div class="question">
        <p><strong>Q{{ loop.index }}. {{ q.text }}</strong></p>
        <div class="choices">
          <label><input type="radio" name="q{{ q.id }}" value="1" required> 1 まったく当てはまらない</label>
          <label><input type="radio" name="q{{ q.id }}" value="2"> 2 あまり当てはまらない</label>
          <label><input type="radio" name="q{{ q.id }}" value="3"> 3 どちらともいえない</label>
          <label><input type="radio" name="q{{ q.id }}" value="4"> 4 やや当てはまる</label>
          <label><input type="radio" name="q{{ q.id }}" value="5"> 5 とても当てはまる</label>
        </div>
      </div>
    {% endfor %}
    <button type="submit">結果を見る</button>
  </form>
</body>
</html>
"""

RESULT_HTML = """
<!doctype html>
<html lang="ja">
<head>
  <meta charset="UTF-8">
  <title>診断結果</title>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
  <style>
    body {
      font-family: sans-serif;
      max-width: 900px;
      margin: 40px auto;
      padding: 0 16px;
      color: #333;
      line-height: 1.7;
    }
    .result {
      margin-top: 32px;
      padding: 20px;
      border: 2px solid #6a5acd;
      border-radius: 10px;
      background: #f7f4ff;
    }
    .score-box {
      margin: 8px 0;
      padding: 10px;
      background: white;
      border-radius: 8px;
      border: 1px solid #ddd;
    }
    .note {
      font-size: 14px;
      color: #666;
    }
    .back-link {
      display: inline-block;
      margin-top: 20px;
    }
    canvas {
      margin-top: 24px;
      background: white;
      border-radius: 8px;
      padding: 8px;
      border: 1px solid #ddd;
    }
  </style>
</head>
<body>
  <h1>診断結果</h1>

  <div class="result">
    <h2>もっとも高いタイプ：{{ highest_type }}</h2>
    <p>{{ comment }}</p>

    <div class="score-box">CP: {{ result["CP"] }} 点</div>
    <div class="score-box">NP: {{ result["NP"] }} 点</div>
    <div class="score-box">A: {{ result["A"] }} 点</div>
    <div class="score-box">FC: {{ result["FC"] }} 点</div>
    <div class="score-box">AC: {{ result["AC"] }} 点</div>

    <canvas id="egoChart" width="400" height="220"></canvas>

    <p class="note">
      点数はあくまで傾向の目安です。高低に良し悪しはなく、バランスを見ることが大切です。
    </p>
  </div>

  <a href="/" class="back-link">もう一度診断する</a>

  <script>
const ctx = document.getElementById('egoChart').getContext('2d');

new Chart(ctx, {
  type: 'line',
  data: {
    labels: ['CP', 'NP', 'A', 'FC', 'AC'],
    datasets: [{
      label: 'エゴグラム',
      data: [
        {{ result["CP"] }},
        {{ result["NP"] }},
        {{ result["A"] }},
        {{ result["FC"] }},
        {{ result["AC"] }}
      ],
      borderColor: '#6a5acd',
      backgroundColor: 'rgba(106,90,205,0.2)',
      fill: false,
      tension: 0.3
    }]
  },
  options: {
    responsive: true,
    scales: {
      y: {
        beginAtZero: true,
        max: 50
      }
    }
  }
});
  </script>
</body>
</html>
"""

@app.route("/", methods=["GET"])
def index():
    shuffled = QUESTIONS.copy()
    random.shuffle(shuffled)
    return render_template_string(INDEX_HTML, questions=shuffled)

@app.route("/result", methods=["POST"])
def result():
    result_scores = {"CP": 0, "NP": 0, "A": 0, "FC": 0, "AC": 0}

    for q in QUESTIONS:
        value = int(request.form.get(f"q{q['id']}", 0))
        result_scores[q["type"]] += value

    highest_key = max(result_scores, key=result_scores.get)
    highest_type = TYPE_LABELS[highest_key]
    comment = TYPE_COMMENTS[highest_key]

    return render_template_string(
        RESULT_HTML,
        result=result_scores,
        highest_type=highest_type,
        comment=comment
    )

if __name__ == "__main__":
    app.run(debug=True)