# MultiThreaded-Proxy-Checker
This tool is designed to efficiently validate proxy servers using multiple threads. It reads proxy lists from files, checks their validity, and writes the working ones back to a file. Whether you need to maintain secure and stable connections through proxies or manage large proxy lists, this tool provides an easy-to-use solution.

## Features

- Multi-threaded proxy validation for improved efficiency.
- Supports reading proxy lists from files for easy integration with existing setups.
- Writes validated proxy servers back to a file for convenient usage.
- Configurable settings for maximum flexibility, including thread count and timeout duration.

## Usage

1. Clone the repository to your local machine.
2. Install the necessary dependencies (Python 3 and requests module).
3. Run the script and follow the instructions to choose your connection method:
   - Direct connection
   - Connection through a proxy with a check of a short list of proxies
   - Connection through a proxy with a check of a large list of proxies
   - Connection through TOR
4. View the logs for information about the validation process and the working proxies found.
5. Utilize the generated file containing the working proxies for your connection needs.

## Requirements

- Python 3
- requests module

## License

This project is licensed under the MIT License with Attribution Copyright (c) [2024] [Dmytro Skyrta] [github.com/dmytro-skyrta].
See the 06 LICENSE.txt file for details.
