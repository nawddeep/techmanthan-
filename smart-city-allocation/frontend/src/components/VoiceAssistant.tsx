"use client";

import { useState, useEffect } from "react";
import { Mic, MicOff } from "lucide-react";

export default function VoiceAssistant() {
  const [listening, setListening] = useState(false);
  const [transcript, setTranscript] = useState("");
  const [supported, setSupported] = useState<boolean | null>(null); // null = not checked yet
  const [showTranscript, setShowTranscript] = useState(false);
  const [recognitionRef, setRecognitionRef] = useState<any>(null);
  const transcriptTimerRef = { current: null as NodeJS.Timeout | null };

  useEffect(() => {
    const SpeechRecognition =
      (window as any).SpeechRecognition ||
      (window as any).webkitSpeechRecognition;

    if (!SpeechRecognition) {
      setSupported(false);
      return;
    }

    setSupported(true);
    const recognition = new SpeechRecognition();
    recognition.continuous = false;
    recognition.interimResults = false;
    recognition.lang = "en-US";

    recognition.onresult = (event: any) => {
      const text = event.results[0][0].transcript.toLowerCase();
      setTranscript(text);
      setShowTranscript(true);
      handleCommand(text);
      setListening(false);
      if (transcriptTimerRef.current) clearTimeout(transcriptTimerRef.current);
      transcriptTimerRef.current = setTimeout(
        () => setShowTranscript(false),
        3000
      );
    };

    recognition.onerror = () => setListening(false);
    recognition.onend = () => setListening(false);

    setRecognitionRef(recognition);
  }, []);

  const speakResponse = (text: string) => {
    if (!("speechSynthesis" in window)) return;
    setTimeout(() => {
      window.speechSynthesis.cancel();
      const utterance = new SpeechSynthesisUtterance(text);
      utterance.rate = 1.0;
      utterance.lang = "en-US";
      const voices = window.speechSynthesis.getVoices();
      const v =
        voices.find((v) => v.lang.startsWith("en-") && v.name.includes("Google")) ||
        voices.find((v) => v.lang.startsWith("en-"));
      if (v) utterance.voice = v;
      window.speechSynthesis.speak(utterance);
    }, 300);
  };

  const handleCommand = (command: string) => {
    if (command.includes("traffic")) {
      document
        .getElementById("traffic-section")
        ?.scrollIntoView({ behavior: "smooth", block: "center" });
      speakResponse("Showing traffic density");
    } else if (command.includes("waste")) {
      document
        .getElementById("waste-section")
        ?.scrollIntoView({ behavior: "smooth", block: "center" });
      speakResponse("Checking waste overflow levels");
    } else if (command.includes("decision")) {
      document
        .getElementById("decision-section")
        ?.scrollIntoView({ behavior: "smooth", block: "center" });
      speakResponse("Opening A.I. decision engine");
    } else {
      speakResponse("Command not recognized, please try again.");
    }
  };

  const toggleListening = () => {
    if (!recognitionRef) return;
    if (listening) {
      recognitionRef.stop();
      setListening(false);
    } else {
      setTranscript("");
      setShowTranscript(false);
      recognitionRef.start();
      setListening(true);
    }
  };

  // Still checking browser support — render nothing to avoid flash
  if (supported === null) return null;

  // Unsupported browser (Firefox, etc.) — hide the button entirely
  // and show a small unobtrusive tooltip instead.
  if (!supported) {
    return (
      <div
        className="fixed bottom-6 right-6 z-[9999]"
        title="Voice assistant requires Chrome or Edge"
      >
        <div className="p-4 rounded-full bg-slate-800/80 border border-slate-700 shadow-lg flex items-center justify-center opacity-40 cursor-not-allowed">
          <MicOffIcon className="w-6 h-6 text-slate-500" />
        </div>
        <span className="absolute -top-8 right-0 bg-slate-900 text-slate-400 text-[10px] px-2 py-1 rounded border border-slate-700 whitespace-nowrap pointer-events-none opacity-0 group-hover:opacity-100 transition-opacity">
          Voice not supported in this browser
        </span>
      </div>
    );
  }

  return (
    <div className="fixed bottom-6 right-6 z-[9999] flex flex-col items-end gap-2">
      {showTranscript && !listening && (
        <div className="bg-slate-900/90 text-slate-200 text-sm px-4 py-2 rounded-xl border border-slate-700 shadow-xl backdrop-blur-md transition-all duration-300">
          You said:{" "}
          <span className="font-semibold text-blue-400">"{transcript}"</span>
        </div>
      )}

      {listening && (
        <div className="bg-blue-600/90 text-white text-sm px-4 py-2 rounded-xl border border-blue-500 shadow-xl backdrop-blur-md animate-pulse">
          Listening…
        </div>
      )}

      <button
        onClick={toggleListening}
        className={`p-4 rounded-full shadow-2xl transition-all duration-300 flex items-center justify-center
          ${
            listening
              ? "bg-rose-500 hover:bg-rose-600 scale-110 shadow-rose-500/50"
              : "bg-blue-600 hover:bg-blue-500 hover:scale-105 shadow-blue-500/20"
          } border border-slate-700/50 hover:shadow-lg`}
        aria-label={listening ? "Stop listening" : "Start voice assistant"}
        title={listening ? "Stop listening" : "Voice assistant (Chrome/Edge)"}
      >
        {listening ? (
          <MicOff className="w-6 h-6 text-white" />
        ) : (
          <Mic className="w-6 h-6 text-white" />
        )}
      </button>
    </div>
  );
}
