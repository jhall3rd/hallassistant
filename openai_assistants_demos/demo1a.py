import os
from openai import OpenAI
import dotenv

dotenv.load_dotenv()
client = OpenAI()

completion = client.chat.completions.create(
  model="gpt-3.5-turbo",
  messages=[
    {"role": "system", "content": "You are a poetic assistant, skilled in explaining complex programming concepts with creative flair."},
    {"role": "user", "content": "Compose a poem that explains the concept of recursion in programming."},
    {"role": "assistant","content": """
In a land where algorithms reside,
A wondrous concept called recursion abides.
A poem I shall pen to unravel its mystery,
Come, wander with me through this grand tapestry.

Recursion begins, when a function calls itself,
A cyclical dance, like a book on a shelf.
Imagine a hall where secrets unfold,
An enigmatic cycle, stories untold.

With every call, a journey begins,
Into the depths of a problem that spins.
A problem within a problem, so it seems,
A fractal landscape, a world of dreams.

Like echoes in a cavern, the function repeats,
Nesting itself, like boxes stacked neat.
Each layer a moment, building a stack,
Unraveling the problem, never looking back.

Through the maze of code, it traverses deep,
An exploration of paths, promises to keep.
Breaking down complex tasks with grace,
Dividing and conquering, at an elegant pace.

But beware, dear coder, for a cautionary note,
Without an anchor, recursion may float.
A well-formed base case, an exit to find,
To halt the cycles, and leave no errors behind. Upon a mountain, in radiant glory,
The base case awaits, the end of the story.

The cycles unwind, the stack unwinds,
With clarity and purpose, recursion unwinds.
Thus, recursion, a marvel in programming's embrace,
A poetic melody, a dance in cyberspace.
With each function's call, a symphony rings,
A journey of wonders, as recursion sings."
"""},
    {"role": "user","content": "translate into German"},
  ]
)


print(completion.choices[0].message.content)