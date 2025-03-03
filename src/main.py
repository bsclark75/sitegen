from blocks import markdown_to_html_node, extract_title
import os
import shutil

def delete_directory_contents(dest_dir):
    """Deletes all contents of the destination directory."""
    for root, dirs, files in os.walk(dest_dir, topdown=False):
        for name in files:
            file_path = os.path.join(root, name)
            print(f"Deleting file: {file_path}")
            os.remove(file_path)
        for name in dirs:
            dir_path = os.path.join(root, name)
            print(f"Deleting directory: {dir_path}")
            os.rmdir(dir_path)

def copy_directory_contents(src_dir, dest_dir):
    """Recursively copies all contents from src_dir to dest_dir."""
    # Ensure the destination directory exists
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

    for item in os.listdir(src_dir):
        src_path = os.path.join(src_dir, item)
        dest_path = os.path.join(dest_dir, item)

        # Check if it's a directory or a file
        if os.path.isdir(src_path):
            # If it's a directory, recursively copy its contents
            print(f"Copying directory: {src_path} to {dest_path}")
            copy_directory_contents(src_path, dest_path)
        else:
            # If it's a file, copy it
            print(f"Copying file: {src_path} to {dest_path}")
            shutil.copy2(src_path, dest_path)  # copy2 preserves metadata (timestamps, etc.)

def clean_and_copy(src_dir, dest_dir):
    """Deletes contents of dest_dir and copies contents from src_dir."""
    # Step 1: Delete all files and subdirectories in the destination directory
    print(f"Cleaning destination directory: {dest_dir}")
    delete_directory_contents(dest_dir)

    # Step 2: Copy all contents from the source directory to the destination directory
    print(f"Copying from {src_dir} to {dest_dir}")
    copy_directory_contents(src_dir, dest_dir)

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path) as markdown_file:
        markdown = markdown_file.read()
    with open(template_path) as template_file:
        template = template_file.read()
    html_nodes = markdown_to_html_node(markdown)
    content = html_nodes.to_html()
    title = extract_title(markdown)
    html = template.replace("{{ Title }}", title)
    html = html.replace("{{ Content }}", content)
    with open(dest_path, "w") as destination_file:
         destination_file.write(html)

def main():
      src_directory = 'static'
      dest_directory = 'public'
      clean_and_copy(src_directory, dest_directory)
      generate_page("content/index.md", "template.html", "public/index.html")

if __name__ == "__main__":
	main()
