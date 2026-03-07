import os
import sys

from dotenv import load_dotenv
from google import genai
from google.genai import types

from prompts import system_prompt
from call_function import available_functions, call_function


def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY environment variable not set")

    args = sys.argv[1:]
    if not args:
        raise RuntimeError("No prompt provided")

    verbose = False
    cleaned_args = []

    for arg in args:
        if arg == "--verbose":
            verbose = True
        else:
            cleaned_args.append(arg)

    if not cleaned_args:
        raise RuntimeError("No prompt provided")

    user_prompt = " ".join(cleaned_args)

    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=user_prompt,
        config=types.GenerateContentConfig(
            tools=[available_functions],
            system_instruction=system_prompt,
            temperature=0,
        ),
    )

    if not response.usage_metadata:
        raise RuntimeError("Gemini API response appears to be malformed")

    print("Prompt tokens:", response.usage_metadata.prompt_token_count)
    print("Response tokens:", response.usage_metadata.candidates_token_count)

    function_results = []

    if response.function_calls:
        for function_call in response.function_calls:
            function_call_result = call_function(function_call, verbose)

            if not function_call_result.parts:
                raise RuntimeError("Function call result has no parts")

            function_response = function_call_result.parts[0].function_response
            if function_response is None:
                raise RuntimeError("Function call result has no function_response")

            if function_response.response is None:
                raise RuntimeError("Function call result has no response")

            function_results.append(function_call_result.parts[0])

            if verbose:
                print(f"-> {function_response.response}")
    else:
        print("Response:")
        print(response.text)


if __name__ == "__main__":
    main()