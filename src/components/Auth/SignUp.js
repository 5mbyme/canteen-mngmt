import React, { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import { getAuth, createUserWithEmailAndPassword } from "firebase/auth";
import { Card, Form, Button, Alert, Container } from "react-bootstrap";

const SignUp = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const [splitEmail, setSplitEmail] = useState("");
  const navigate = useNavigate();

  const validateEmail = (email) => {
    const re = /^\w+([.-]?\w+)*@\w+([.-]?\w+)*(\.\w{2,3})+$/;
    return re.test(String(email).toLowerCase());
  };

  const handleEmailChange = (e) => {
    setEmail(e.target.value);
    setSplitEmail(e.target.value.split("@")[0] || "");
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!validateEmail(email)) {
      setError("Invalid email format");
      return;
    }
    try {
      setError("");
      setLoading(true);
      const auth = getAuth();
      await createUserWithEmailAndPassword(auth, email, password);
      navigate("/");
    } catch (err) {
      setError("Failed to create an account: " + err.message);
    }
    setLoading(false);
  };

  return (
    <Container
      className="d-flex align-items-center justify-content-center"
      style={{ minHeight: "100vh" }}
    >
      <div className="w-100" style={{ maxWidth: "400px" }}>
        <Card className="rounded-4">
          <Card.Body>
            <h2 className="mb-4 p-2 fw-bold">Sign Up</h2>
            {error && <Alert variant="danger">{error}</Alert>}
            <Form onSubmit={handleSubmit}>
              {email && (
                <div className="d-flex justify-content-center mb-3">
                  <img
                    src={`https://ui-avatars.com/api/?name=${splitEmail}&background=random`}
                    alt={`Profile avatar for ${splitEmail}`}
                    className="rounded-circle"
                    width="100"
                    height="100"
                  />
                </div>
              )}
              <Form.Group className="mb-3">
                <Form.Label htmlFor="signup-email">Email</Form.Label>
                <Form.Control
                  type="email"
                  id="signup-email"
                  value={email}
                  onChange={handleEmailChange}
                  required
                  aria-label="Email address"
                  aria-required="true"
                />
              </Form.Group>
              <Form.Group className="mb-3">
                <Form.Label htmlFor="signup-password">Password</Form.Label>
                <Form.Control
                  type="password"
                  id="signup-password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  required
                  aria-label="Password"
                  aria-required="true"
                />
              </Form.Group>
              <Button
                disabled={loading}
                className="w-100 rounded-4"
                type="submit"
                aria-label="Submit sign up form"
              >
                Sign Up
              </Button>
            </Form>
          </Card.Body>
        </Card>
        <div className="w-100 text-center mt-2">
          Already have an account?{" "}
          <Link to="/login" className="text-decoration-none" aria-label="Navigate to login page">
            Log In
          </Link>
        </div>
      </div>
    </Container>
  );
};

export default SignUp;
