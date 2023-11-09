from prompt_toolkit import prompt, print_formatted_text, HTML


def main():
    text = ""
    while True:
        try:
            text = prompt('Give me some input: ')
            if text.strip().startswith("!q"):
                print_formatted_text(HTML('<ansigreen>bye</ansigreen>'))
                return
            text = text.strip()
            if text:
                print_formatted_text(HTML(f'You said: <aaa fg="ansiwhite" bg="skyblue">{text}</aaa>'))
        except EOFError:
            print_formatted_text(HTML("<ansired>bye</ansired>"))
            return

if __name__ == "__main__":
    main()