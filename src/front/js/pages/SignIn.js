import React, { useState } from 'react';
import { Link } from 'react-router-dom';

const SignIn = () => {
    const [passwordShown, setPasswordShown] = useState(false);

    const togglePasswordVisibility = () => {
        setPasswordShown(!passwordShown);
    };

    return (
        <div className="overlay">
            <form>
                <div className="con">
                    <header className="head-form">
                        <h2>Sign In</h2>
                        <p>Enter the information to sign in</p>
                    </header>
                    <br />
                    <div className="field-set">
                        <span className="input-item">
                            <i className="fa-solid fa-envelope"></i>
                        </span>
                        <input className="form-input" id="txt-input1" type="text" placeholder="Email" required />
                        <br />
                        <span className="input-item">
                            <i className="fa fa-user-circle"></i>
                        </span>
                        <input className="form-input" id="txt-input2" type="text" placeholder="Username" required />
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
                        <button className="log-in">Sign In</button>
                    </div>
                    <Link to="/login">
                        <button className="btn submits sign-up">
                            Log in
                            <i className="fa-solid fa-arrow-right-to-bracket"></i>
                        </button>
                    </Link>
                </div>
            </form>
        </div>
    );
};

export default SignIn;
