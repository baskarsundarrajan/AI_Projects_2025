"use client";

import React, { useState, useEffect } from "react";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { Divide, Upload } from "lucide-react";
import apiClient from "@/components/service/axios";
import Questions from "@/components/questions";
import { firebaseApp,auth,db } from "@/components/service/firebase";
import { collection, addDoc, doc, setDoc } from "firebase/firestore";
// import { v4 as uuidv4 } from "uuid"; // For random test ID


export default function QuizApp() {
    const hehe = async ()=>{
    let code_id = "12300"
    let userId = auth.currentUser.uid
    const codesRef = doc(db, 'tests', userId, 'codes',code_id);
    setDoc(codesRef, {
      "questions":["q1","q2","q3"],
    }).then((res)=>{
        console.log("created successfully",res);
        
    });
    
    
    }
    return(
        <div>
            <p>click this button</p>
            <Button onClick={hehe}>HELLO</Button>
        </div>
    )
}