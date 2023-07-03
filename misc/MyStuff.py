import misc.ax as ax 
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



def xy(st):
  return ax.xxxxy(st)

