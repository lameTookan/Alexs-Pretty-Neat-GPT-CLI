class fg:
  black = "\u001b[30m"
  red = "\u001b[31m"
  green = "\u001b[32m"
  yellow = "\u001b[33m"
  blue = "\u001b[34m"
  magenta = "\u001b[35m"
  cyan = "\u001b[36m"
  white = "\u001b[37m"
  reset = "\u001b[0m"

  def rgb(r, g, b): return f"\u001b[38;2;{r};{g};{b}m"

class bg:
  black = "\u001b[40m"
  red = "\u001b[41m"
  green = "\u001b[42m"
  yellow = "\u001b[43m"
  blue = "\u001b[44m"
  magenta = "\u001b[45m"
  cyan = "\u001b[46m"
  white = "\u001b[47m"


  def rgb(r, g, b): return f"\u001b[48;2;{r};{g};{b}m"

colors_fg = {
    "black": "\u001b[30m",
    "red": "\u001b[31m",
    "green": "\u001b[32m",
    "yellow": "\u001b[33m",
    "blue": "\u001b[34m",
    "magenta": "\u001b[35m",
    "cyan": "\u001b[36m",
    "white": "\u001b[37m",
    "rgb": lambda r, g, b: f"\u001b[38;2;{r};{g};{b}m"
}

colors_bg = {
    "black": "\u001b[40m",
    "red": "\u001b[41m",
    "green": "\u001b[42m",
    "yellow": "\u001b[43m",
    "blue": "\u001b[44m",
    "magenta": "\u001b[45m",
    "cyan": "\u001b[46m",
    "white": "\u001b[47m"
}
def yellow(text):
  return f"{fg.yellow}{text}{fg.reset}"
def red(text):
  return f"{fg.red}{text}{fg.reset}"
def green(text):
  return f"{fg.green}{text}{fg.reset}"
def blue(text):
  return f"{fg.blue}{text}{fg.reset}"
def magenta(text):
  return f"{fg.magenta}{text}{fg.reset}"
def cyan(text):
  return f"{fg.cyan}{text}{fg.reset}"
def white(text):
  return f"{fg.white}{text}{fg.reset}"
def underline(text):
	return f"\u001b[4m{text}{fg.reset}"
def bold(text):
	return f"\u001b[1m{text}{fg.reset}"
def italic(text):
	return f"\u001b[3m{text}{fg.reset}"
def print_colors(text):
	for color in colors_fg:
		print(f"{colors_fg[color]}{text}{fg.reset}")

	

dividers_basic = {
	"dash": "-"*50,
	"dot": "."*50,
	"tilda" : "~"*50,
	"underscore": "_"*50,
	"*": "*"*50,
	"equal": "="*50,
	"hash": "#"*50,
	"pipe": "|"*50,
	"plus": "+"*50,
	"minus": "-"*50,
}
dividers_neat = {
	"night": "•☽────✧˖°˖☆˖°˖✧────☾•",
	"star": "───── ⋆⋅☆⋅⋆ ─────",
	"cat": "=^..^=   =^..^=   =^..^=    =^..^=    =^..^=    =^..^=    =^..^=", 
	"geo": "nunununununununununununununununununununununununununununununun",
	"oOo": ".oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.",
	'basic': "+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+","smiley": "☹☻☹☻☹☻☹☻☹☻☹☻☹☻☹☻☹☻☹☻☹",
	"diamond": "--:::------::------------------->◇<--------------------::------:::---",
	"temple": "╬╬═════════════╬╬", 
	"bell": "▂ ▃ ▄ ▅ ▆ ▇ █ █ ▇ ▆ ▅ ▄ ▃ ▂",
	"skull": "☠◉☠◉☠◉☠◉☠◉☠◉☠◉☠◉☠◉☠◉☠◉☠◉☠",
	"fancy": "▅▄▃▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▂▃▄▅",
	"double": "══════════════════════════════════════════════════════"
	
}
dividers = {

}
dividers.update(dividers_basic)
dividers.update(dividers_neat)
def print_all_dividers():
	for divider in dividers:
		print(dividers[divider])
def print_divider(divider_name="basic"):
	text = dividers.get(divider_name, "invalid")
	print(text)
def get_divider(divider_name="basic"):
	text = dividers.get(divider_name, "invalid")
	return text


nicki_minaj = """
Pull up in the monster, automobile gangsta
With a bad bitch that came from Sri Lanka
Yeah, I'm in that Tonka, color of Willy Wonka
You could be the king but watch the Queen conquer
Okay, first things first I'll eat your brains
Then I'ma start rockin' gold teeth and fangs
'Cause that's what a motherfuckin' monster do
Hairdresser from Milan, that's the monster 'do
Monster Giuseppe heel, that's the monster shoe
Young money is the roster and the monster crew
And I'm all up, all up, all up in the bank with the funny face
And if I'm fake, I ain't notice 'cause my money ain't
So let me get this straight, wait, I'm the rookie?
But my features and my shows ten times your pay?
Fifty K for a verse, no album out
Yeah, my money's so tall that my Barbies gotta climb it
Hotter than a Middle Eastern climate, violent
Tony Matterhorn, dutty wine it, wine it
Nicki on them titties when I sign it
That's how these [the_dev_is_white] so one-track minded
But really, really I don't give a F-U-C-K
"Forget Barbie, fuck Nicki 'cause sh-she's fake"
"She on a diet, " but my pockets eatin' cheesecake
And I'll say bride of Chucky is child's play
Just killed another career it's a mild day
Besides, Ye, they can't stand besides me
I think me, you and Amb' should ménage Friday
Pink wig, thick ass, give 'em whip lash
I think big, get cash, make 'em blink fast
Now look at what you just saw, this is what you live for
Ah, I'm a motherfuckin' monster"""