#include <cstdlib>
#include <iostream>

int main() {
    // Define the Python script path
    std::string script_path = "python d:\\CGVR\\CP\\Backend\\test.py";

    // Run the Python script using system()
    int result = std::system(script_path.c_str());

    // Check the result
    if (result == 0) {
        std::cout << "Python script executed successfully!" << std::endl;
    } else {
        std::cerr << "Failed to execute Python script. Error code: " << result << std::endl;
    }

    return 0;
}
