
import React, { useState } from 'react';
import axios from 'axios';
import './index.css';

function App() {
  const [jobInput, setJobInput] = useState({
    title: '',
    description: '',
    requirements: '',
    role: '',
  });
  const [jobId, setJobId] = useState('');
  const [response, setResponse] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setJobInput({ ...jobInput, [name]: value });
  };

  const handleJobIdChange = (e) => {
    setJobId(e.target.value);
  };

  const runWorkflow = async (payload) => {
    setLoading(true);
    setError('');
    setResponse(null);
    try {
      const res = await axios.post('http://127.0.0.1:5000/run_agent', payload, {
        headers: { 'Content-Type': 'application/json' },
      });
      setResponse(res.data.result);
    } catch (err) {
      setError('Error running workflow: ' + (err.response?.data?.error || err.message));
    } finally {
      setLoading(false);
    }
  };

  const createJob = () => {
    if (!jobInput.title || !jobInput.description || !jobInput.requirements || !jobInput.role) {
      setError('Please fill in all job fields');
      return;
    }
    const requirements = jobInput.requirements.split(',').map((req) => req.trim());
    runWorkflow({ ...jobInput, requirements });
  };

  const runExistingJob = () => {
    if (!jobId) {
      setError('Please enter a Job ID');
      return;
    }
    runWorkflow({ job_id: parseInt(jobId) });
  };

  return (
    <div className="container">
      <h1>Agentic Hiring Bot</h1>

      {/* Create New Job */}
      <div className="card mb-4">
        <div className="card-header">Create New Job</div>
        <div className="card-body">
          <div className="mb-3">
            <label htmlFor="title" className="form-label">Job Title</label>
            <input
              type="text"
              className="form-control"
              name="title"
              placeholder="Enter job title"
              value={jobInput.title}
              onChange={handleInputChange}
            />
          </div>
          <div className="mb-3">
            <label htmlFor="description" className="form-label">Description</label>
            <textarea
              className="form-control"
              name="description"
              placeholder="Enter job description"
              value={jobInput.description}
              onChange={handleInputChange}
            />
          </div>
          <div className="mb-3">
            <label htmlFor="requirements" className="form-label">Requirements (comma-separated)</label>
            <input
              type="text"
              className="form-control"
              name="requirements"
              placeholder="Enter requirements (e.g., Python, Flask)"
              value={jobInput.requirements}
              onChange={handleInputChange}
            />
          </div>
          <div className="mb-3">
            <label htmlFor="role" className="form-label">Role</label>
            <input
              type="text"
              className="form-control"
              name="role"
              placeholder="Enter role (e.g., Hiring Manager)"
              value={jobInput.role}
              onChange={handleInputChange}
            />
          </div>
          <button className="btn btn-primary" onClick={createJob} disabled={loading}>
            {loading ? 'Creating...' : 'Create Job'}
          </button>
        </div>
      </div>

      {/* Run Existing Job */}
      <div className="card mb-4">
        <div className="card-header">Run Workflow for Existing Job</div>
        <div className="card-body">
          <div className="mb-3">
            <label htmlFor="jobId" className="form-label">Job ID</label>
            <input
              type="number"
              className="form-control"
              placeholder="Enter Job ID"
              value={jobId}
              onChange={handleJobIdChange}
            />
          </div>
          <button className="btn btn-primary" onClick={runExistingJob} disabled={loading}>
            {loading ? 'Running...' : 'Run Workflow'}
          </button>
        </div>
      </div>

      {/* Loading Spinner */}
      {loading && (
        <div className="text-center my-3">
          <div className="spinner-border" role="status">
            <span className="visually-hidden">Loading...</span>
          </div>
          <p>Running workflow...</p>
        </div>
      )}

      {/* Error Alert */}
      {error && <div className="alert alert-danger">{error}</div>}

      {/* Results */}
      {response && (
        <div className="results">
          <h2>Workflow Results</h2>
          <div className="accordion" id="resultsAccordion">
            {/* Job Details */}
            <div className="accordion-item">
              <h2 className="accordion-header">
                <button className="accordion-button" type="button" data-bs-toggle="collapse" data-bs-target="#jobDetails">
                  Job Details
                </button>
              </h2>
              <div id="jobDetails" className="accordion-collapse collapse show" data-bs-parent="#resultsAccordion">
                <div className="accordion-body">
                  <p><strong>Job ID:</strong> {response.job_id || 'N/A'}</p>
                  <p><strong>Title:</strong> {response.title || 'N/A'}</p>
                  <p><strong>Description:</strong> {response.description || 'N/A'}</p>
                  <p><strong>Requirements:</strong> {response.requirements ? response.requirements.join(', ') : 'N/A'}</p>
                  <p><strong>Role:</strong> {response.role || 'N/A'}</p>
                  <p><strong>Status:</strong> {response.final_status || 'N/A'}</p>
                </div>
              </div>
            </div>
            {/* Applicants */}
            <div className="accordion-item">
              <h2 className="accordion-header">
                <button className="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#applicants">
                  Applicants
                </button>
              </h2>
              <div id="applicants" className="accordion-collapse collapse" data-bs-parent="#resultsAccordion">
                <div className="accordion-body">
                  {Array.isArray(response.applicants) && response.applicants.length ? (
                    <ul className="list-group">
                      {response.applicants.map((a) => (
                        <li className="list-group-item" key={a.id}>
                          <strong>{a.name || 'N/A'}</strong> (ID: {a.id || 'N/A'})<br />
                          Email: {a.email || 'N/A'}<br />
                          Resume: <a href={a.resume_link || '#'} target="_blank" rel="noopener noreferrer">{a.resume_link || 'N/A'}</a><br />
                          Score: {a.score || 'N/A'}
                        </li>
                      ))}
                    </ul>
                  ) : (
                    <p>No applicants found.</p>
                  )}
                </div>
              </div>
            </div>
            {/* Shortlisted Applicants */}
            <div className="accordion-item">
              <h2 className="accordion-header">
                <button className="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#shortlisted">
                  Shortlisted Applicants
                </button>
              </h2>
              <div id="shortlisted" className="accordion-collapse collapse" data-bs-parent="#resultsAccordion">
                <div className="accordion-body">
                  {Array.isArray(response.shortlisted_applicants) && response.shortlisted_applicants.length ? (
                    <p>Candidate IDs: {response.shortlisted_applicants.join(', ')}</p>
                  ) : (
                    <p>No candidates shortlisted.</p>
                  )}
                </div>
              </div>
            </div>
            {/* Interview Schedules */}
            <div className="accordion-item">
              <h2 className="accordion-header">
                <button className="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#interviews">
                  Interview Schedules
                </button>
              </h2>
              <div id="interviews" className="accordion-collapse collapse" data-bs-parent="#resultsAccordion">
                <div className="accordion-body">
                  {Array.isArray(response.interview_results) && response.interview_results.length ? (
                    <ul className="list-group">
                      {response.interview_results.map((r) => (
                        <li className="list-group-item" key={r.candidate_id}>
                          <strong>{r.candidate_name || 'N/A'}</strong> (ID: {r.candidate_id || 'N/A'})<br />
                          Time: {r.interview_time || 'N/A'}<br />
                          Status: {r.status || 'N/A'}
                        </li>
                      ))}
                    </ul>
                  ) : (
                    <p>No interviews scheduled.</p>
                  )}
                </div>
              </div>
            </div>
            {/* Interview Simulations */}
            <div className="accordion-item">
              <h2 className="accordion-header">
                <button className="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#simulations">
                  Interview Simulations
                </button>
              </h2>
              <div id="simulations" className="accordion-collapse collapse" data-bs-parent="#resultsAccordion">
                <div className="accordion-body">
                  {Array.isArray(response.interview_simulation_results) && response.interview_simulation_results.length ? (
                    <ul className="list-group">
                      {response.interview_simulation_results.map((r) => (
                        <li className="list-group-item" key={r.candidate_id}>
                          <strong>{r.candidate_name || 'N/A'}</strong> (ID: {r.candidate_id || 'N/A'})<br />
                          Status: {r.status || 'N/A'}<br />
                          Questions: {r.questions || 'N/A'}
                        </li>
                      ))}
                    </ul>
                  ) : (
                    <p>No interview simulations conducted.</p>
                  )}
                </div>
              </div>
            </div>
            {/* Decision */}
            <div className="accordion-item">
              <h2 className="accordion-header">
                <button className="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#decision">
                  Decision
                </button>
              </h2>
              <div id="decision" className="accordion-collapse collapse" data-bs-parent="#resultsAccordion">
                <div className="accordion-body">
                  <p><strong>Decision:</strong> {response.decision || 'N/A'}</p>
                </div>
              </div>
            </div>
            {/* Offers */}
            <div className="accordion-item">
              <h2 className="accordion-header">
                <button className="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#offers">
                  Offers
                </button>
              </h2>
              <div id="offers" className="accordion-collapse collapse" data-bs-parent="#resultsAccordion">
                <div className="accordion-body">
                  {Array.isArray(response.offer_results) && response.offer_results.length ? (
                    <ul className="list-group">
                      {response.offer_results.map((o) => (
                        <li className="list-group-item" key={o.candidate_id}>
                          <strong>{o.candidate_name || 'N/A'}</strong> (ID: {o.candidate_id || 'N/A'})<br />
                          Status: {o.status || 'N/A'}<br />
                          Offer Letter: <pre>{o.offer_letter || 'N/A'}</pre>
                        </li>
                      ))}
                    </ul>
                  ) : (
                    <p>No offers sent.</p>
                  )}
                </div>
              </div>
            </div>
            {/* Regrets */}
            <div className="accordion-item">
              <h2 className="accordion-header">
                <button className="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#regrets">
                  Regrets
                </button>
              </h2>
              <div id="regrets" className="accordion-collapse collapse" data-bs-parent="#resultsAccordion">
                <div className="accordion-body">
                  {Array.isArray(response.regret_results) && response.regret_results.length ? (
                    <ul className="list-group">
                      {response.regret_results.map((r) => (
                        <li className="list-group-item" key={r.candidate_id}>
                          <strong>{r.candidate_name || 'N/A'}</strong> (ID: {r.candidate_id || 'N/A'})<br />
                          Status: {r.status || 'N/A'}
                        </li>
                      ))}
                    </ul>
                  ) : (
                    <p>No regret emails sent.</p>
                  )}
                </div>
              </div>
            </div>
            {/* Onboarding */}
            <div className="accordion-item">
              <h2 className="accordion-header">
                <button className="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#onboarding">
                  Onboarding
                </button>
              </h2>
              <div id="onboarding" className="accordion-collapse collapse" data-bs-parent="#resultsAccordion">
                <div className="accordion-body">
                  {Array.isArray(response.onboarding_results) && response.onboarding_results.length ? (
                    <ul className="list-group">
                      {response.onboarding_results.map((o) => (
                        <li className="list-group-item" key={o.candidate_id}>
                          <strong>{o.candidate_name || 'N/A'}</strong> (ID: {o.candidate_id || 'N/A'})<br />
                          Status: {o.status || 'N/A'}
                        </li>
                      ))}
                    </ul>
                  ) : (
                    <p>No onboarding instructions sent.</p>
                  )}
                </div>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default App;
