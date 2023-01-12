import React, { createContext, useEffect, useState } from "react";
import axios from "axios";
import { BASEURL } from "../config/URLs";

export const AppContext = createContext()

export const AppProvider = ({ children }) => {
    //STATEFUL VARIABLES
    const [waitingOnResponse, setWaitingOnResponse] = useState(false)
    
    const AnalyzeImage = (base64, width, height) => {
        axios.post(`${BASEURL}/analyze`, { image: base64, width, height })
        .then(res => {
            //setWaitingOnResponse(true)
            console.log(res.data)
        }).catch(e => {
            console.log(`Failed To Save Image: ${e}`)
        })
    }

    //STARTUP FUNCTIONS
    useEffect(() => {
        
    }, [])

    return (
        <AppContext.Provider value={{ waitingOnResponse, AnalyzeImage }}>
            {children}
        </AppContext.Provider>
    )
}