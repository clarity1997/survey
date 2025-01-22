from flask import Flask, render_template_string, request

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        responses = request.form
        return render_template_string(confirmation_template, responses=responses)
    return render_template_string(form_template)

form_template = """
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <title>Survey on Green Finance and New Productivity</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
            overflow-y: scroll;
            background: linear-gradient(135deg, #6B73FF 0%, #000DFF 100%);
            color: white;
            text-align: center;
            animation: backgroundMove 10s infinite alternate;
        }
        @keyframes backgroundMove {
            0%, 100% { background-position: left bottom; }
            50% { background-position: right top; }
        }

        .container {
            margin: auto;
            padding: 20px;
            width: 90%;
            max-width: 800px;
            background: rgba(0, 0, 0, 0.6);
            border-radius: 10px;
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
            margin-top: 40px;
            margin-bottom: 40px;
        }

        h1, h2, h3 {
            margin-bottom: 20px;
        }

        h1 { font-size: 2.5em; }
        h2 { font-size: 2em; }

        label {
            display: block;
            text-align: left;
            margin-bottom: 5px;
            font-size: 1.1em;
        }

        input[type="submit"] {
            background-color: #4CAF50;
            border: none;
            color: white;
            padding: 10px 20px;
            text-align: center;
            text-decoration: none;
            display: inline-block;
            font-size: 1em;
            margin: 10px 0;
            cursor: pointer;
            border-radius: 5px;
        }

        .question {
            margin-bottom: 25px;
        }

        .answer-options {
            margin-top: 10px;
            text-align: left;
        }

        .answer-options input {
            margin-right: 10px;
        }
    </style>
  </head>
  <body>
    <div class="container">
        <h1>綠色金融與新質生產力調查問卷</h1>
        <form method="post">
            {% for question in questions %}
            <div class="question">
                <label>{{ question['text'] }}</label>
                <div class="answer-options">
                    {% for option in question['options'] %}
                        <input type="{{ question['type'] }}" name="{{ question['name'] }}" value="{{ option }}"> {{ option }}<br>
                    {% endfor %}
                </div>
            </div>
            {% endfor %}
            <input type="submit" value="提交">
        </form>
    </div>
  </body>
</html>
"""

confirmation_template = """
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <title>Survey Submitted</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
            overflow-y: scroll;
            background: linear-gradient(135deg, #6B73FF 0%, #000DFF 100%);
            color: white;
            text-align: center;
            animation: backgroundMove 10s infinite alternate;
        }
        @keyframes backgroundMove {
            0%, 100% { background-position: left bottom; }
            50% { background-position: right top; }
        }

        .container {
            margin: auto;
            padding: 20px;
            width: 90%;
            max-width: 800px;
            background: rgba(0, 0, 0, 0.6);
            border-radius: 10px;
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
            margin-top: 40px;
            margin-bottom: 40px;
        }

        h1 {
            margin-bottom: 20px;
            font-size: 2.5em;
        }

        p {
            text-align: left;
            font-size: 1.1em;
        }
    </style>
  </head>
  <body>
    <div class="container">
        <h1>感谢您的参与！</h1>
        <p>您的问卷已提交成功。以下是您的回答：</p>
        <ul>
            {% for key, value in responses.items() %}
            <li><strong>{{ key }}:</strong> {{ value }}</li>
            {% endfor %}
        </ul>
    </div>
  </body>
</html>
"""

@app.context_processor
def inject_questions():
    questions = [
        {"text": "貴公司對「綠色金融」的認知程度如何？", "type": "radio", "name": "q1", "options": ["非常了解", "比較了解", "一般了解", "不太了解", "完全不了解"]},
        {"text": "貴公司是否曾經使用過綠色金融服務？", "type": "radio", "name": "q2", "options": ["是", "否"]},
        {"text": "貴公司認為綠色金融對於企業的發展有多重要？", "type": "radio", "name": "q3", "options": ["非常重要", "比較重要", "一般重要", "不太重要", "完全不重要"]},
        {"text": "您認為未來綠色金融的發展潛力如何？", "type": "radio", "name": "q4", "options": ["非常有潛力", "比較有潛力", "一般有潛力", "不太有潛力", "沒有潛力"]},
        {"text": "貴公司選擇使用綠色金融的主要驅動因素是什麼？", "type": "checkbox", "name": "q5", "options": ["符合環保政策", "提高公司形象", "獲取資金支持", "降低運營成本", "其他（請指明）"]},
        {"text": "在採用綠色金融時，貴公司面臨的主要挑戰是什麼？", "type": "checkbox", "name": "q6", "options": ["資金不足", "缺乏技術支持", "經營風險高", "缺乏市場信息", "其他（請指明）"]},
        {"text": "您認為綠色金融服務對促進新質生產力的作用如何？", "type": "radio", "name": "q7", "options": ["非常有幫助", "比較有幫助", "一般有幫助", "不太有幫助", "完全沒幫助"]},
        {"text": "綠色金融服務如何支持和促進您公司的新質生產力？", "type": "checkbox", "name": "q8", "options": ["提供資金支持", "促進技術創新", "提高市場競爭力", "降低運營風險", "其他（請指明）"]},
        {"text": "貴公司是否計劃在未來增加對綠色金融的投資？", "type": "radio", "name": "q9", "options": ["是", "否"]},
        {"text": "貴公司在綠色金融方面的投資策略是什麼？", "type": "checkbox", "name": "q10", "options": ["減少碳排放", "提高能源效率", "發展可再生能源", "支持環保技術", "其他（請指明）"]},
        {"text": "您認為政府應出台哪些政策支持企業參與綠色金融？", "type": "checkbox", "name": "q11", "options": ["稅收優惠", "資金補助", "技術支持", "法律保障", "其他（請指明）"]},
        {"text": "為促進綠色金融發展，您公司有什麼建議給金融機構？", "type": "checkbox", "name": "q12", "options": ["降低貸款利率", "增加綠色金融產品類型", "提供專業諮詢", "強化市場宣傳", "其他（請指明）"]},
        {"text": "貴公司對「新質生產力」的認知程度如何？", "type": "radio", "name": "q13", "options": ["非常了解", "比較了解", "一般了解", "不太了解", "完全不了解"]},
        {"text": "貴公司目前是否在實踐新質生產力？", "type": "radio", "name": "q14", "options": ["是", "否"]},
        {"text": "貴公司認為新質生產力最重要的驅動因素是什麼？", "type": "checkbox", "name": "q15", "options": ["技術創新", "市場需求", "政府政策", "成本效益", "其他（請指明）"]},
        {"text": "貴公司實施新質生產力時遇到的主要挑戰是什麼？", "type": "checkbox", "name": "q16", "options": ["資金限制", "技術不足", "人才匱乏", "管理困難", "其他（請指明）"]},
        {"text": "貴公司在新質生產力方面採取了哪些具體措施？", "type": "checkbox", "name": "q17", "options": ["採用智能製造", "進行流程優化", "使用新材料", "推進自動化", "其他（請指明）"]},
        {"text": "您認為新質生產力的實踐對貴公司產生了哪些成效？", "type": "checkbox", "name": "q18", "options": ["提高生產效率", "降低成本", "增加利潤", "提升產品質量", "其他（請指明）"]},
        {"text": "您認為香港在新質生產力方面的競爭力如何？", "type": "radio", "name": "q19", "options": ["非常競爭力", "比較競爭力", "一般競爭力", "不太競爭力", "完全不競爭力"]},
        {"text": "您認為香港在新質生產力方面有哪些獨特的優勢？", "type": "checkbox", "name": "q20", "options": ["科技創新中心", "先進的基礎設施", "高效的金融體系", "強大的法制保護", "其他（請指明）"]}
    ]
    return dict(questions=questions)

if __name__ == "__main__":
    app.run(debug=True)

