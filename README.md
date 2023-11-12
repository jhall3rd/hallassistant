# Some basic demos of OpenAI's Assistant framework

1. demo1.py -- generate poetry
2. demo2.py -- solve a tricky math problem

    One response is:

    ```text
    [messages]
    text: I need to solve the equation `sin(x) + cos(x) + 11 = 14`. Can you help me?
    [/messages]
    [messages]
    text: Certainly! The equation you've provided is `sin(x) + cos(x) + 11 = 14`. The first step to solve this is to simplify the equation by moving the constant terms to one side:

    `sin(x) + cos(x) + 11 = 14`
    `sin(x) + cos(x) = 14 - 11`
    `sin(x) + cos(x) = 3`

    This equation involves solving for x where the sum of the sine and cosine of x equals 3. 
    However, we know that the maximum value of `sin(x)` and `cos(x)` is 1, and since they can't 
    both be 1 at the same time, the sum of these two functions should not exceed √2, 
    which is approximately 1.414. Therefore, any real value of x that would make `sin(x) + cos(x)` equal 
    to 3 is impossible because the sum of their maximum values does not reach 3.

    The equation has no solution in the real number domain. However, if you are looking for complex 
    solutions, that would involve more advanced methods that go beyond the scope of typical 
    trigonometric solutions.

    If you meant to solve for real solutions within the usual bounds of sine and cosine functions, 
    the answer is that there are no such solutions. 

    Would you like to revisit the equation or inquire about complex solutions?
    [/messages]
    ```
    This is undoubtedly a good answer. Sometimes, it goes ahead and solves the equation.
    Very reasonable, because there are complex domain solutions. 

    
3. demo3.py -- solve an easier math problem, but use asyncio for practice.

    ```text
   [messages]
    text: I need to solve the equation `6x + 11 = 14`. Can you help me?
    [/messages]
    [messages]
    text: I need to solve the equation `6x + 11 = 14`. Can you help me?
    text: The solution to the equation 6x + 11 = 14 is x = 1/2.
    [/messages]
    ```


4. demo4.py -- function calling via assistant interface.
    ```
   [messages]
    text: What's the weather in Point Scramble, New Brunswick?
    [/messages]
    [messages]
    text: What's the weather in Point Scramble, New Brunswick?
    text: The current weather in Point Scramble, New Brunswick is -4°C. Please let me know if there is anything else you need, Jane Doe.
    [/messages]
   ```
   

5, demo5.py -- simple interactive loop.

   ```
[H] what's the weather in London?
[A] The current weather in London is 12 degrees Celsius, Alfred Clement.
[H] how about Paris
[A] The current weather in Paris is 15 degrees Celsius, Alfred Clement.
[H] how about Washington, Delaware?
[A] The current weather in Washington, Delaware, is 1 degree Celsius, Alfred Clement.
[H] Jakarta?
[A] The current weather in Jakarta is 20 degrees Celsius, Alfred Clement.
[H] Jamaica?
[A] The current weather in Jamaica is 3 degrees Celsius, Alfred Clement. However, this seems quite unusual as Jamaica is typically much warmer. It could be a mistake or an anomaly. Please let me know if I can assist you further.
[H] Atlantis?
[A] Atlantis is a legendary island mentioned in the works of the Greek philosopher Plato. It's not a real location that can have a current weather report. Plato's stories are the only known source of information about this mythical place, and there is no evidence Atlantis ever existed. If you have another location whose weather you'd like to check, please let me know!
[H] bye
[A] bye
   ```




Consistent problem solving is not guaranteed. That's how these things are.

To run these you need an OpenAI key, and you should place it in a file called .env
in the following format
```text
OPENAI_API_KEY=<your_key>
```