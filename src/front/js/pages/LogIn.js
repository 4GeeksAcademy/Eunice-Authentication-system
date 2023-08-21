import React, { useState } from 'react';

const LogIn = () => {
  const [passwordShown, setPasswordShown] = useState(false);

  const togglePasswordVisibility = () => {
    setPasswordShown(!passwordShown);
  };

  return (
    <div className="overlay">
      <form>
        <div className="con">
          <header className="head-form">
            <h2>Log In</h2>
            <p>Enter the information to log in</p>
          </header>
          <br />
          <div className="field-set">
            <span className="input-item">
              <i className="fa fa-user-circle"></i>
            </span>
            <input className="form-input" id="txt-input" type="text" placeholder="Username" required />
            <br />
            <span className="input-item">
              <i className="fa fa-key"></i>
            </span>
            <input
              className="form-input"
              type={passwordShown ? "text" : "password"}
              placeholder="Password"
              id="pwd"
              name="password"
              required
            />
            <span>
              <i className={`fa ${passwordShown ? "fa-eye-slash" : "fa-eye"}`} type="button" id="eye" onClick={togglePasswordVisibility}></i>
            </span>
            <br />
            <button className="log-in">Log In</button>
          </div>
          <button className="btn submits sign-up">
            Sign Up
            <i className="fa fa-user-plus"></i>
          </button>
        </div>
      </form>
    </div>
  )
}

export default LogIn
