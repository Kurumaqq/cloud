import { useNavigate } from "react-router-dom";
import { useState } from "react";
import classes from "./Login.module.css";
import axios from "axios";
import config from "../../../public/config.json";

export default function LoginForm() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const navigate = useNavigate();

  const handleClick = () => {
    axios
      .post(
        `${config.APIURL}/login`,
        { username, password },
        { withCredentials: true }
      )
      .then((response) => {
        navigate("/root");
      })
      .catch((error) => {
        console.log(error);
      });
  };

  return (
    <main className={classes.login}>
      <form className={classes.form}>
        <h1 className={classes.subtitle}>Welcome!</h1>

        <label className={classes.label} htmlFor="username">
          Login
        </label>
        <input
          className={classes.input}
          placeholder="Enter Login"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          type="text"
          id="username"
          name="username"
        />

        <label className={classes.label} htmlFor="password">
          Password
        </label>
        <input
          className={classes.input}
          placeholder="Enter Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          type="password"
          id="password"
          name="password"
        />

        <button onClick={handleClick} type="button" className={classes.button}>
          Login
        </button>
      </form>
    </main>
  );
}
