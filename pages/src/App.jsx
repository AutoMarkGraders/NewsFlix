import { useState } from 'react'
import './App.css'
import Heading from './components/Heading/Heading';
import Left from './components/Left/Left';
import Right from './components/Right/Right';
import Card from './components/ui/Card';

const App = () => {

  return ( 
    <div id="App">
      <Heading />
      
      <Right />
      <Left />
    </div>
  )
};

export default App
