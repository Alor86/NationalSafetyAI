from flask import Flask, request, redirect, url_for, render_template_string
from twilio.rest import Client

app = Flask(__name__)

# Replace with your Twilio Account SID and Auth Token
TWILIO_ACCOUNT_SID = ''TWILIO_ACCOUNT_SID''
TWILIO_AUTH_TOKEN = ''TWILIO_AUTH_TOKEN''

# Your Twilio phone number and recipient number (with country codes)
TWILIO_PHONE_NUMBER = '+18064040853'
ALERT_PHONE_NUMBER = '+919346050631'

client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

HOME_HTML = '''
<!doctype html>
<title>Emergency Alert System</title>
<h2>Type "fire" or "factory" to trigger alerts</h2>
<form method="post">
  <input type="text" name="keyword" autofocus required>
  <input type="submit" value="Send Alert">
</form>
<p>{{ message }}</p>
'''

FIRE_ALERT_HTML = '''
<!doctype html>
<html>
<head>
<title>Fire Alert Activated</title>
</head>
<body>
<h1>Fire Alert Activated</h1>
<video id="alertVideo" width="640" height="360" autoplay muted>
  <source src="{{ url_for('static', filename='fire_alert_video.mp4') }}" type="video/mp4">
  Your browser does not support the video tag.
</video>
<script>
const synth = window.speechSynthesis;
const messages = [
  'Warning fire detected, fire detected, evacuate immediately.',
  'Activating Arjun.'
];

function speakMessages(index = 0) {
  if (index >= messages.length) {
    document.getElementById('alertVideo').muted = false;
    return;
  }
  const utterance = new SpeechSynthesisUtterance(messages[index]);
  utterance.onend = () => speakMessages(index + 1);
  synth.speak(utterance);
}

window.onload = () => {
  speakMessages();
};
</script>
</body>
</html>
'''

FACTORY_ALERT_HTML = '''
<!doctype html>
<html>
<head>
<title>Factory Alert Activated</title>
</head>
<body>
<h1>Factory Alert Activated</h1>
<video id="alertVideo" width="800" height="450" autoplay muted>
  <source src="{{ url_for('static', filename='factory_demo_video.mp4') }}" type="video/mp4">
  Your browser does not support the video tag.
</video>
<script>
const synth = window.speechSynthesis;
const messages = [
  'Attention! A critical event has been detected at the factory site.',
  'Please follow all safety protocols immediately.',
  'Activating emergency control units.',
  'Observe the demonstration video to understand emergency procedures.'
];

function speakMessages(index = 0) {
  if (index >= messages.length) {
    document.getElementById('alertVideo').muted = false;
    return;
  }
  const utterance = new SpeechSynthesisUtterance(messages[index]);
  utterance.onend = () => speakMessages(index + 1);
  synth.speak(utterance);
}

window.onload = () => {
  speakMessages();
};
</script>
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def index():
    message = ''
    if request.method == 'POST':
        keyword = request.form.get('keyword', '').strip().lower()
        try:
            if keyword == 'fire':
                client.calls.create(
                    twiml='<Response><Say>Warning fire detected, fire detected, evacuate immediately. Activating Arjun.</Say></Response>',
                    to=ALERT_PHONE_NUMBER,
                    from_=TWILIO_PHONE_NUMBER
                )
                return redirect(url_for('alert_page'))
            elif keyword == 'factory':
                client.calls.create(
                    twiml='<Response><Say>Attention! A critical event has been detected at the factory site. Please follow all safety protocols immediately.</Say></Response>',
                    to=ALERT_PHONE_NUMBER,
                    from_=TWILIO_PHONE_NUMBER
                )
                return redirect(url_for('factory_alert'))
            else:
                message = "Invalid keyword. Type 'fire' or 'factory' to send alert."
        except Exception as e:
            message = f"Failed to send call: {e}"

    return render_template_string(HOME_HTML, message=message)

@app.route('/alert')
def alert_page():
    return render_template_string(FIRE_ALERT_HTML)

@app.route('/factory_alert')
def factory_alert():
    return render_template_string(FACTORY_ALERT_HTML)

if __name__ == '__main__':
    app.run(debug=True)
