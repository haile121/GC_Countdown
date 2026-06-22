import json
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

FUNNY_MESSAGES: list[str] = [
    "Why did the IS student cross the road? To optimize the shortest path algorithm.",
    "Why do IS students make great chefs? They know how to handle NULL values in their recipes.",
    "An IS student's love life: 'It's complicated' — just like their ER diagrams.",
    "I told my database I loved it. It said: 'ERROR: Relationship not found.'",
    "Why did the IS student break up with Excel? Too many unresolved dependencies.",
    "Our ERP system has more modules than I have brain cells — and both crash regularly.",
    "I asked my professor for help. He said: 'Have you tried turning it off and on again?'",
    "IS students don't have bugs, we have 'undocumented features'.",
    "Why do IS students never get lost? They always follow the network topology.",
    "Real drama is having a feature that's totally not working… and your evaluator's be like, Can you show me that one? ",
    "My GPA and my RAM have one thing in common: never enough.",
    "I don't always test my code, but when I do, I do it in production.",
    "An IS student's diet: coffee, Chat Gpt, and existential dread.",
    "Why did the IS student stare at the orange juice? The box said 'concentrate'.",
    "Our group project has more merge conflicts than a highway at rush hour.",
    "I finally understood recursion. I finally understood recursion. I finally understood recursion.",
    "Why do IS students make bad secret keepers? They always normalize everything.",
    "My code works perfectly — on my machine. Shipping my machine.",
    "IS students don't sleep, they enter low-power mode.",
    "Why did the IS student fail the cooking class? Kept trying to JOIN the ingredients.",
    "I have 99 problems and a missing semicolon is definitely one of them.",
    "Our professor said 'think outside the box'. I said 'which box — the server or the VM?'",
    "Why do IS students make great detectives? They always trace the stack.",
    "I named my Wi-Fi 'Graduation' so my laptop is always connected to the goal.",
    "IS students don't procrastinate — we just implement lazy evaluation.",
    "Why did the IS student bring a ladder to class? To reach the cloud.",
    "My code works. I have no idea why."
    "IS students don't have nightmares, we have infinite loops.",
    "Why do IS students love the beach? Excellent bandwidth and no firewall.",
    "I asked the IT support guy for help. He asked me to describe my problem. I said: 'Where do I start?'",
    "IS students don't age — we just get deprecated.",
]

INSPIRATIONAL_MESSAGES: list[str] = [
    "Every problem you've solved has upgraded the person you're becoming.",
    "You've learned to think in systems. Now go build a better one.",
    "Graduation isn't the end of learning — it's the beginning of applying it.",
    "You are more capable than any system you've ever designed.",
    "The world is full of problems waiting for an IS graduate to solve them.",
    "Success is just a well-executed project plan — and you've been planning this for years.",
    "You've mastered the art of turning complexity into clarity. That's rare.",
    "The best is yet to come. Your graduation is just version 1.0.",
    "Every exam you passed was a proof of concept. Now it's time for production.",
    "You've built the foundation. Now go build the future on top of it.",
    "IS taught you that every problem has a solution — and you have the tools to find it.",
    "Your potential is not limited by your current resources. Scale up.",
    "The world needs people who understand both technology and humanity. That's exactly you.",
    "Graduation is your go-live date. The system is ready. Deploy with confidence.",
    "Every line of code you've written is a step closer to the career you've been building.",
    "Systems fail, but IS graduates adapt — that's your superpower.",
    "You've debugged harder problems than this. Graduation is just the final deployment.",
    "The knowledge you've gained isn't stored in RAM — it's permanent.",
    "Every database you've designed has taught you to structure your future.",
    "You didn't come this far to only come this far. Keep pushing.",
    "The best systems are built by people who never stop learning — that's you.",
    "Your degree is the architecture; your career is the implementation.",
    "Information Systems taught you to solve problems. Life is just a bigger problem set.",
    "You've survived group projects, finals, and legacy code. You can survive anything.",
    "The finish line is in sight. Don't stop now — the system is almost deployed.",
    "Every challenge you've faced has been a feature, not a bug, in your growth.",
    "You are the bridge between technology and people — the world needs that.",
    "Your hard work is compiling. The output is a bright future.",
    "IS graduates don't just use technology — they shape it.",
    "Every late night studying was an investment with a guaranteed return.",
    "The skills you've built are your most valuable assets. Invest in them daily.",
]


class MessageCycler:
    """Cycles through a list of messages, persisting the current index to a JSON file."""

    def __init__(self, messages: list[str], state_key: str, state_file: str = "cycle_state.json"):
        if not messages:
            raise ValueError("messages list must not be empty")
        self._messages = messages
        self._state_key = state_key
        self._state_file = Path(state_file)
        self._index = self._load_index()

    def _load_index(self) -> int:
        try:
            data = json.loads(self._state_file.read_text())
            idx = int(data.get(self._state_key, 0))
            return idx % len(self._messages)
        except (FileNotFoundError, json.JSONDecodeError, ValueError, TypeError):
            logger.warning(
                "cycle_state.json missing or corrupt for key '%s'; resetting to 0.",
                self._state_key,
            )
            return 0

    def _save_index(self) -> None:
        try:
            try:
                data = json.loads(self._state_file.read_text())
            except (FileNotFoundError, json.JSONDecodeError):
                data = {}
            data[self._state_key] = self._index
            self._state_file.write_text(json.dumps(data))
        except OSError as exc:
            logger.error("Failed to persist cycle state: %s", exc)

    def next(self) -> str:
        """Returns the next message in the cycle and advances the index."""
        message = self._messages[self._index]
        self._index = (self._index + 1) % len(self._messages)
        self._save_index()
        return message

    def current_index(self) -> int:
        return self._index
