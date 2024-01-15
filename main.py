import requests
from bs4 import BeautifulSoup
from sendEmail import send_email


def find_product_sizes(product_links):
    sizes_dict = {}

    for product_link in product_links:
        try:
            response = requests.get(product_link, headers={
                                    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"})
            response.raise_for_status()

            soup = BeautifulSoup(response.content, "lxml")
            size_picker = soup.find("div", {"id": "size-picker"})

            if size_picker:
                sizes = []
                for child in size_picker.find_all(recursive=False):
                    size_info = child.find_all(recursive=False)[2].find_all(
                        recursive=False)[1].get_text().split(' ')[1]
                    sizes.append(size_info)
                sizes_dict[product_link] = [int(size) for size in sizes]
            else:
                sizes_dict[product_link] = ["Size picker not found"]

        except requests.RequestException as e:
            sizes_dict[product_link] = [f"Error: {e}"]

    return sizes_dict


def format_product_sizes(product_sizes):
    formatted_product_sizes = ""
    for key, value in product_sizes.items():
        formatted_product_sizes += f"{key}: {value}\n"
    return formatted_product_sizes


product_links = open("product-links.txt").read().splitlines()
sizes_you_want = [3, 8, 9]


def main():
    try:
        product_sizes = find_product_sizes(product_links)
        for _, sizes in product_sizes.items():
            for size in sizes:
                if size in sizes_you_want:
                    # ek v product ka size mil gya toh email bhej do
                    send_email("Status of the puma products you wanna buy",
                               format_product_sizes(product_sizes))
                    quit()

        send_email("Your puma products not found",
                   f"I couldn't find the puma products you wanted in stock. Thank you!\n\n{format_product_sizes(product_sizes)}")
    except Exception as e:
        print(e)
        send_email("Error in the puma products you wanna buy",
                   "There was an error in the puma products you wanted to buy. Thank you!\n\nCheck your logs for more info :()")


if __name__ == "__main__":
    main()
