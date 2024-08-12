"""
This module contains the JavaScripts class, which provides various JavaScript snippets for interacting with web elements using Selenium WebDriver.
"""


class JavaScripts:
    """
    JavaScripts class provides a collection of JavaScript snippets for various web element interactions.

    Attributes:
        HIGHLIGHT_ELEMENT (str): JavaScript to highlight an element by adding a red border.
        SCROLL_TO_ELEMENT (str): JavaScript to scroll to the bottom of an element.
        SCROLL_INTO_VIEW (str): JavaScript to scroll an element into the center of the viewport.
        SCROLL_WITH_LENGTH (str): JavaScript to scroll the window by a specified length.
        GET_ELEMENT_HIGHT (str): JavaScript to get the top position of an element relative to the viewport.
        OPEN_NEW_WINDOW (str): JavaScript to open a new browser window.
        IS_ELEMENT_VISIBLE (str): JavaScript to check if an element is visible and centered within the viewport.
        CREATE_BLUE_DOT (str): JavaScript to create a blue dot that follows the cursor.
        GET_CURSOR_COORDS (str): JavaScript to get the current cursor coordinates.
        MOVE_CURSOR_AND_CREATE_DOT (str): JavaScript to move the cursor to specified coordinates and create a blue dot.
        PERFORM_MOUSE_CLICK (str): JavaScript to move the cursor to specified coordinates and perform a mouse click.
    """

    HIGHLIGHT_ELEMENT = "arguments[0].style.border='3px solid red'"

    SCROLL_TO_ELEMENT = "arguments[0].scrollTop = arguments[0].scrollHeight;"

    SCROLL_INTO_VIEW = "arguments[0].scrollIntoView({block: 'center'});"

    SCROLL_WITH_LENGTH = "window.scrollBy(0, arguments[0]);"

    GET_ELEMENT_HIGHT = "return arguments[0].getBoundingClientRect().top"

    OPEN_NEW_WINDOW = "window.open('');"

    IS_ELEMENT_VISIBLE = """
            var elem = arguments[0], box = elem.getBoundingClientRect();
            var viewportWidth = (window.innerWidth || document.documentElement.clientWidth);
            var viewportHeight = (window.innerHeight || document.documentElement.clientHeight);
            
            // Calculate element's center
            var elemCenterX = box.left + (box.width / 2);
            var elemCenterY = box.top + (box.height / 2);
            
            // Calculate viewport's center
            var viewportCenterX = viewportWidth / 2;
            var viewportCenterY = viewportHeight / 2;
            
            // Calculate tolerance in pixels
            var toleranceX = viewportWidth * arguments[1];
            var toleranceY = viewportHeight * arguments[1];
            
            // Check if the element's center is within the tolerance of the viewport's center
            var isCenteredHorizontally = Math.abs(elemCenterX - viewportCenterX) <= toleranceX;
            var isCenteredVertically = Math.abs(elemCenterY - viewportCenterY) <= toleranceY;
            
            return isCenteredHorizontally && isCenteredVertically && 
                box.top < viewportHeight && box.bottom >= 0 &&
                box.left < viewportWidth && box.right >= 0;
        """

    CREATE_BLUE_DOT = """
        function createBlueDot() {
            document.addEventListener('mousemove', function(e) {
                // Remove existing dot if any
                const existingDot = document.getElementById('cursor-dot');
                if (existingDot) {
                    existingDot.remove();
                }

                // Create a new dot
                const dot = document.createElement('div');
                dot.id = 'cursor-dot';
                dot.style.position = 'absolute';
                dot.style.width = '10px';
                dot.style.height = '10px';
                dot.style.backgroundColor = 'blue';
                dot.style.borderRadius = '50%';
                dot.style.left = e.pageX + 'px';
                dot.style.top = e.pageY + 'px';
                dot.style.zIndex = '1000';
                document.body.appendChild(dot);
            });
        }
        createBlueDot();
        """

    GET_CURSOR_COORDS = """
        function getCursorPosition() {
            return new Promise((resolve) => {
                document.addEventListener('mousemove', function handler(e) {
                    document.removeEventListener('mousemove', handler); // Remove the handler after getting the position
                    resolve({ x: e.pageX, y: e.pageY });
                });
            });
        }
        return getCursorPosition();
        """

    MOVE_CURSOR_AND_CREATE_DOT = """
        function moveCursorAndCreateDot(x, y) {
            // Create a new dot
            const dot = document.createElement('div');
            dot.id = 'cursor-dot';
            dot.style.position = 'absolute';
            dot.style.width = '10px';
            dot.style.height = '10px';
            dot.style.backgroundColor = 'blue';
            dot.style.borderRadius = '50%';
            dot.style.left = x + 'px';
            dot.style.top = y + 'px';
            dot.style.zIndex = '1000';

            // Remove existing dot if any
            const existingDot = document.getElementById('cursor-dot');
            if (existingDot) {
                existingDot.remove();
            }

            // Append the new dot to the body
            document.body.appendChild(dot);

            // Simulate moving the cursor
            const event = new MouseEvent('mousemove', {
                view: window,
                bubbles: true,
                cancelable: true,
                clientX: x,
                clientY: y
            });
            document.dispatchEvent(event);
        }

        // Example usage
        moveCursorAndCreateDot(arguments[0], arguments[1]);
        """

    PERFORM_MOUSE_CLICK = """
        function moveCursorAndClick(x, y) {
            // Simulate moving the cursor
            const moveEvent = new MouseEvent('mousemove', {
                view: window,
                bubbles: true,
                cancelable: true,
                clientX: x,
                clientY: y
            });
            document.dispatchEvent(moveEvent);

            // Simulate a mouse click
            const clickEvent = new MouseEvent('click', {
                view: window,
                bubbles: true,
                cancelable: true,
                clientX: x,
                clientY: y
            });
            document.dispatchEvent(clickEvent);
        }

        // Example usage
        moveCursorAndClick(arguments[0], arguments[1]);
        """
