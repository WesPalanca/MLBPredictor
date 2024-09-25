import axios from "axios";
import { useState } from "react";

const Predict = () =>{
    const [team, setTeam] = useState("");
    const [opp, setOpp] = useState("");
    const [ha, setHA] = useState("home"); 
    const [modelPrediction, setModelPrediction] = useState();
    const [predictionProba, setPredictionProba] = useState();
    const makePrediction = async (e) =>{
        e.preventDefault();
        try{
            const response = await axios.post("http://localhost:8080/api/predict", {
                team: team,
                opp: opp,
                "h/a": ha
            });
            const {prediction, prediction_proba} = response.data;
            setModelPrediction(prediction);
            setPredictionProba(prediction_proba);
            console.log(prediction);
            console.log(predictionProba);
        }
        catch(error){
            console.log(error);
        }
        
    };

    return (
        <div className="Predict">
            <form onSubmit={makePrediction}>
                <input type="text" value={team} onChange={(e) => setTeam(e.target.value)} placeholder="Your team abbr   " />
                <input type="text" value={opp} onChange={(e) => setOpp(e.target.value)} placeholder="Your opponent abbr"/>
                <select value={ha} onChange={(e) => setHA(e.target.value)}>
                    <option value="home">Home</option>
                    <option value="away">Away</option>
                </select>
                
                <button type="submit">Make Prediction</button>
            </form>
        </div>
    )

};




export default Predict;