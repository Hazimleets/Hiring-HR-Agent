
from flask import Flask, request, jsonify
from flask_cors import CORS
from db.schema import db, Job, Candidate
from config import Config
from agents.agent import run_agent
from db.seed import seed_data
import logging

app = Flask(__name__)
# Configure CORS to allow frontend origins
CORS(app, resources={r"/run_agent": {"origins": ["http://localhost:3000", "http://localhost:3001"]}})
# Enable debug logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Config
app.config['SQLALCHEMY_DATABASE_URI'] = Config.DB_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

with app.app_context():
    # Create tables and seed data
    db.create_all()
    seed_data(db)
    logger.debug("Jobs: %s", Job.query.all())
    logger.debug("Candidates: %s", Candidate.query.all())

@app.route('/')
def index():
    return {"message": "Chatbot 4 (Agentic Hiring Bot) is running."}

@app.route('/run_agent', methods=['POST'])
def run_agent_route():
    if not request.is_json:
        logger.error("Request must be JSON")
        return jsonify({"error": "Request must be JSON"}), 400
    input_data = request.get_json()
    if not input_data:
        logger.error("Empty JSON payload")
        return jsonify({"error": "Empty JSON payload"}), 400
    logger.debug("Received input_data: %s", input_data)
    try:
        response = run_agent(input_data)
        logger.debug("run_agent response: %s", response)
        return jsonify(response)
    except Exception as e:
        logger.error("Error in run_agent: %s", str(e))
        return jsonify({"error": f"Agent error: {str(e)}"}), 500

@app.teardown_appcontext
def shutdown_session(exception=None):
    db.session.remove()

if __name__ == '__main__':
    logger.info("✅ Starting Chatbot 4 (Agentic Hiring Bot)")
    app.run(debug=Config.DEBUG)
