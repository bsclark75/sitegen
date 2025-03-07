from blocks import markdown_to_html_node, extract_title
import os
import shutil
import sys

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

def generate_page(from_path, template_path, dest_path, base_path="/"):
    if os.path.isdir(from_path):
        if not os.path.exists(dest_path):
            os.makedirs(dest_path)
        print(f"Entering directory: {from_path}")
        for entry in os.listdir(from_path):
            full_path = os.path.join(from_path, entry)
            dest_full_path = os.path.join(dest_path, entry)
            if os.path.isdir(full_path):
            # Recursive call to process subdirectories
                generate_page(full_path, template_path, dest_full_path, base_path)
            else:
                process_markdown_file(full_path, template_path, dest_full_path, base_path)
    else:
        process_markdown_file(from_path, template_path, dest_path, base_path)

def process_markdown_file(from_file, templatefile, dest_file, base_path="/"):
    filename,ext = dest_file.split(".")
    dest_file = filename + ".html"
    print(f"Generating page from {from_file} to {dest_file} using {templatefile}")
    with open(from_file) as markdown_file:
        markdown = markdown_file.read()
    with open(templatefile) as template_file:
        template = template_file.read()
    html_nodes = markdown_to_html_node(markdown)
    #print(html_nodes)
    content = html_nodes.to_html()
    title = extract_title(markdown)
    html = template.replace("{{ Title }}", title)
    html = html.replace("{{ Content }}", content)
    html = html.replace('href="/', f'href="/{base_path}')
    html = html.replace('src="/', f'src="/{base_path}')
    with open(dest_file, "w") as destination_file:
         destination_file.write(html)

def main():
      basepath = sys.argv[1]
      src_directory = 'static'
      dest_directory = 'docs'
      clean_and_copy(src_directory, dest_directory)
      generate_page("content", "template.html", "docs", basepath)

if __name__ == "__main__":
	main()
