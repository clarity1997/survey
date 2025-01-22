from flask import Flask, request, render_template_string

app = Flask(__name__)

html_template = """
<!DOCTYPE html>
<html>
<head>
    <title>香港企業新質生產力和綠色金融問卷調查</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            background: linear-gradient(45deg, #0f2027, #2c5364, #203a43, #0f2027);
            color: #fff;
            animation: GradientBackground 10s ease infinite;
            background-size: 400% 400%;
            overflow-x: hidden;
        }
        @keyframes GradientBackground {
            0% {
                background-position: 0% 50%;
            }
            50% {
                background-position: 100% 50%;
            }
            100% {
                background-position: 0% 50%;
            }
        }
        container {
            display: flex;
            justify-content: center;
            align-items: center;
            flex-direction: column;
            padding: 20px;
        }
        form {
            background: rgba(255, 255, 255, 0.1);
            border-radius: 16px;
            padding: 20px;
            width: 80%;
            max-width: 600px;
            box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
            backdrop-filter: blur(4px);
            -webkit-backdrop-filter: blur(4px);
        }
        h1, h2, h3 {
            text-align: center;
        }
        .question {
            margin: 15px 0;
        }
        label {
            display: block;
            margin: 5px 0;
        }
        input[type="text"], textarea {
            width: 100%;
            padding: 10px;
            margin-top: 5px;
        }
        input[type="submit"] {
            margin: 10px 0;
            padding: 12px 20px;
            border: none;
            border-radius: 4px;
            background: #4CAF50;
            color: white;
            font-size: 16px;
            cursor: pointer;
        }
        input[type="submit"]:hover {
            background: #45a049;
        }
    </style>
</head>
<body>
    <container>
        <form method="POST">
            <h1>香港企業新質生產力和綠色金融問卷調查</h1>
            <p>我們感謝您參加這次調查，以助我們了解香港企業在新質生產力和綠色金融方面的狀況。這些問題旨在收集您的寶貴意見和經驗。您的回應將會被保密並僅用於研究目的。</p>

            <h2>一. 企業背景信息</h2>
            <div class="question">
                <label>1. 您的企業所在行業是？</label>
                <select name="industry">
                    <option value="manufacturing">製造業</option>
                    <option value="finance">金融業</option>
                    <option value="trade_logistics">貿易及物流業</option>
                    <option value="other">其他 (請註明)</option>
                </select>
            </div>
            <div class="question">
                <label>2. 您的企業員工人數是？</label>
                <select name="employees">
                    <option value="less_than_50">少於50人</option>
                    <option value="50_to_100">50-100人</option>
                    <option value="100_to_500">100-500人</option>
                    <option value="more_than_500">多於500人</option>
                </select>
            </div>

            <h2>二. 新質生產力</h2>
            <h3>認知度和重要性</h3>

            <!-- Add more questions here as specified -->

            <div>
                <h2>三. 綠色金融</h2>
                <h3>ESG目標設立</h3>
                <div class="question">
                    <label>11. 您的企業是否設立了ESG（環境、社會和公司治理）相關目標？</label>
                    <select name="esg_goals">
                        <option value="yes">是</option>
                        <option value="no">否</option>
                    </select>
                </div>

                <div class="question" id="esg_yes" style="display: none;">
                    <label>12.（如設立ESG目標，問：） 您的企業設立了哪些ESG目標？（請具體說明）</label>
                    <textarea name="esg_specific_goals"></textarea>
                </div>

                <div class="question" id="esg_no" style="display: none;">
                    <label>13.（如未設立ESG目標，問：） 為什麼您的企業沒有設立ESG目標？</label>
                    <select name="esg_reason_no">
                        <option value="lack_of_understanding">缺乏了解</option>
                        <option value="high_cost">成本過高</option>
                        <option value="lack_of_resources">缺乏資源</option>
                        <option value="other">其他 (請註明)</option>
                    </select>
                    <textarea name="other_esg_reason"></textarea>
                </div>
            </div>
            <input type="submit" value="提交">
        </form>
    </container>

    <script>
        document.addEventListener('change', function(e) {
            let esgGoals = document.querySelector('select[name="esg_goals"]').value;
            if (esgGoals === 'yes') {
                document.getElementById('esg_yes').style.display = 'block';
                document.getElementById('esg_no').style.display = 'none';
            } else if (esgGoals === 'no') {
                document.getElementById('esg_yes').style.display = 'none';
                document.getElementById('esg_no').style.display = 'block';
            } else {
                document.getElementById('esg_yes').style.display = 'none';
                document.getElementById('esg_no').style.display = 'none';
            }
        });
    </script>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # You can access the form data here and process it as needed
        data = request.form.to_dict()
        return f"Thanks for submitting the survey! You submitted: {data}"

    return render_template_string(html_template)

if __name__ == '__main__':
    app.run(debug=True)

