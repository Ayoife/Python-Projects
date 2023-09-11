import React from 'react';
import "./App.css"


function Info() {
    const UI = (
        <div className="info">
            <h2 className="card--name">Ayinde-Oladeinde Ayoife</h2>
            <h3 className="card--job">Frontend Developer</h3>
            <a href="https://ayoife.github.com"
                className="card--website">
                ayoife.github.com</a>
        </div>)

    return UI;
}

function Contact() {
    const UI = (
        <div className="contact">
            <a className="email-btn" href="http://www.gmail.com">Email</a>
            <a className="linkedin-btn" href="http://www.linkedin.com">LinkedIn</a>
        </div>)

    return UI;
}

function About() {
    const UI = (
        <div className="about">
            <h2 className="title">About</h2>
            <p>
                I am a frontend developer with a particular interest in making
                things simple and automating daily tasks. I try to keep up with security
                and best practices, and I'm always looking for new things to learn ;)
            </p>
        </div>)

    return UI;
}

function Interests() {
    const UI = (
        <div className="interests">
            <h2 className="title">Interests</h2>
            <p>
                Food expert, Music Scholar, Reader, Internet fanatic, Travel geek,
                Coffee fanatic, Movie fanatic and lots more ;)
            </p>
        </div>)

    return UI;
}

function Icons() {
    const UI = (
        <ul className="socials">
            <li>F</li>
            <li>T</li>
            <li>I</li>
            <li>G</li>
        </ul>)

    return UI;
}

export default function App() {

    const noOfImages = 4;
    const [imgIndex, setImgIndex] = React.useState(0);
    const [theme, setTheme] = React.useState(0);

    function changePhoto() {
        setImgIndex(prevValue => { return (prevValue + 1) % noOfImages })
    }

    function changeTheme() {
        setTheme(prevValue => { return prevValue === 0 ? 1 : 0 })
    }

    console.log(imgIndex)
    const UI = (
        <div className={`card ${theme === 0 ? "light" : "dark"}`}>
            <img src={`./images/me${imgIndex === 0 ? '' : ` ${imgIndex}`}.jpg`}
                alt="Ayoife"
                width="300px"
                onClick={changePhoto} />
            <div onClick={changeTheme} className="card-body">
                <Info theme={theme} />
                <Contact theme={theme} />
                <About theme={theme} />
                <Interests theme={theme} />
            </div>
            <Icons />
        </div>);

    return UI;
}