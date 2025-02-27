from textnode import TextNode

def main():
	textnode = TextNode("This is a text node", "bold", "https:/www.boot.dev")
	othernode = TextNode("This is a text node", "bold", "https:/www.boot.dev")
	print(textnode)
	if textnode == othernode:
		print("The eq function worked")
	else:
		print("The eq function did not work")

if __name__ == "__main__":
	main()
