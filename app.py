from flask import Flask, request, jsonify
from flask_cors import CORS
from twilio.rest import Client
import os

app = Flask(__name__)
CORS(app)

TWILIO_SID   = 'AC768768e06c77e879e9751298a79bf265'
TWILIO_TOKEN = '8e17a4b15d28f6786d0ee797bb58d040'
TWILIO_FROM  = '+15017462670'

@app.route('/')
def home():
    return jsonify({'status': 'fluent backend is live!'})

@app.route('/call', methods=['POST'])
def make_call():
    data = request.json
    to_number = data.get('to')
    if not to_number:
        return jsonify({'error': 'no number provided'}), 400

    twiml = """<Response>
  <Say voice="Polly.Joanna">
    Hey! This is your Fluent English coach.
    Ready to practice? Tell me what you worked on today at work. Go ahead!
  </Say>
</Response>"""

    try:
        client = Client(TWILIO_SID, TWILIO_TOKEN)
        call = client.calls.create(
            to=to_number,
            from_=TWILIO_FROM,
            twiml=twiml
        )
        return jsonify({'success': True, 'sid': call.sid})
    except Exception as ex:
        return jsonify({'error': str(ex)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
