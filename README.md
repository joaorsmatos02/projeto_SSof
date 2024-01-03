# Discovering vulnerabilities in Python web applications


## Overview

This project is aimed at achieving an in-depth understanding of security issues in Python web applications.

##Unsanitized Flows: Implementation Note

The current representation of unsanitized_flows may not accurately reflect the intended logic due to time constraints in completing the implementation. The envisioned approach involves leveraging a dedicated class to handle unsanitized flows.

The proposed logic dictates that when a combination occurs, the unsanitized flow for a variable or function should be set to "yes" if any combined element has an unsanitized flow of "yes." Conversely, it would be set to "no" only if all the variables involved in the combination have an unsanitized flow of "no."

For variables that serve as the sole source in a label, we set the unsanitized flow to "no" when a sanitizer is added. This rule aims to signify that, in the absence of other sources, the addition of a sanitizer guarantees a sanitized flow.


## Tests

The project underwent a series of tests to evaluate its functionality and robustness. The majority of the tests produced successful results, validating the effectiveness of the implemented features. However, one specific test, `9-regions-guards.py`, encountered an issue during execution.

### Test Results

- **Test 1 to Test 8 (Passed):**
  - Description: Each of these tests validated different aspects of the project, and all of them passed successfully.
  - Results: Successful

- **Test 9 (Failed): `9-regions-guards.py`**
  - Description: This test specifically targets the behavior of the project when executing `9-regions-guards.py`.
  - Results: Failed
  - Explanation: The failure in this test is attributed to the inside `if` condition within the while loop. When the while loop runs more than once, it triggers the condition in a way that causes the test to fail. The intricate details of this failure are under investigation to ensure the reliability of the project under varying conditions.

These test results provide insights into the project's overall performance and highlight areas for improvement, particularly in the context of the `9-regions-guards.py` test.

## Running the Project

```bash
# Example command to run the project
python ./py_analyser.py <path_to_slice>\<slice>.py .<path_to_slice>\<slice>.patterns.json
```
It will output as requested.

## Contributors
 - **Diogo Pereira**    - 110996
 - **João Santos**      - 110947
 - **João Matos**       - 110846

