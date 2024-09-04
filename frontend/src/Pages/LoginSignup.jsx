import { useState } from "react";
import axios from 'axios';
const LoginSignup = () =>{
    const [loginData, setLoginData] = useState({
        username: "",
        password: ""
    });

    const [registerData, setRegisterData] = useState({
            email: "",
            username: "",
            first_name: "",
            last_name: "",
            password: ""
    })
    const [formToggle, setFormToggle] = useState(true);
    const handleLoginSubmit = (e) =>{
        e.preventDefault();
        console.log(loginData);

    }
    const handleRegisterSubmit = async (e) =>{
        e.preventDefault();
        try{
            const response = await axios.post('http://localhost:8080/api/users/register',{
               email: registerData.email,
               first_name: registerData.first_name,
               last_name: registerData.last_name,
               username: registerData.username,
               password: registerData.password 
            });
        }
        catch(error){
            console.log(error);
        }
    }
    const onLoginChange = (e) =>{
        setLoginData({...loginData, [e.target.id]: e.target.value})
    }
    const onRegisterChange = (e) =>{
        setRegisterData({...registerData, [e.target.id]: e.target.value})
    }
    return(
       <div className="Page">

         {formToggle ?
            <form className="form" onSubmit={handleLoginSubmit}>
                <p><strong>Log in</strong></p>
                <input type="text" id="username" placeholder="username" value={loginData.username} onChange={onLoginChange} required={true} />
                <input type="password" id="password" placeholder="password" value={loginData.password} onChange={onLoginChange} required={true} />
                <button type="submit">Login</button> 
                <button onClick={() => setFormToggle(false)}>Create Account</button>

            </form> :

            <form className="form" onSubmit={handleRegisterSubmit}>
                <p><strong>Register</strong></p>
                <input type="email" placeholder="email" id="email" value={registerData.email} onChange={onRegisterChange} />
                <input type="text" placeholder="first name" id="first_name" value={registerData.first_name} onChange={onRegisterChange} />
                <input type="text" placeholder="last name" id="last_name" value={registerData.last_name} onChange={onRegisterChange} />
                <input type="text" id="username" placeholder="username"  value={registerData.username} onChange={onRegisterChange} required={true} />
                <input type="text" id="password" placeholder="password" value={registerData.password} onChange={onRegisterChange} required={true} />
                <button type="submit">Register</button>
                <button onClick={() => setFormToggle(true)}>Already have an account?</button>

            </form> 
            }
       </div>
    )
}




export default LoginSignup;