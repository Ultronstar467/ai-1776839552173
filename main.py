from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

# Configure CORS middleware
origins = [
    "http://127.0.0.1:5500",  # Or whatever port your live-server runs on
    "http://localhost:5500",
    "http://127.0.0.1:8000",
    "http://localhost:8000",
    # Add other origins if your frontend is hosted elsewhere
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory storage for game state (for simplicity)
# In a real application, this would be a database
game_state = {
    "high_score": 0
}

class ScoreData(BaseModel):
    score: int

@app.get("/game/state")
async def get_game_state():
    """
    Retrieves the current game state, including the high score.
    """
    return {"high_score": game_state["high_score"]}

@app.post("/game/end")
async def end_game(data: ScoreData):
    """
    Endpoint called when a game ends.
    Updates the high score if the submitted score is higher.
    """
    if data.score < 0:
        raise HTTPException(status_code=400, detail="Score cannot be negative")

    if data.score > game_state["high_score"]:
        game_state["high_score"] = data.score
        print(f"New high score: {game_state['high_score']}")
    
    return {"message": "Game ended", "score_submitted": data.score, "high_score": game_state["high_score"]}

@app.get("/")
async def root():
    return {"message": "Welcome to the Snake Game API"}