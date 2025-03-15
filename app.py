import json
import streamlit as st

class PersonalLibraryManager:
    def __init__(self):
        self.library = []
        self.filename = "library.json"
        self.load_library()

    def load_library(self):
        """Load library data from a file."""
        try:
            with open(self.filename, "r") as file:
                self.library = json.load(file)
        except FileNotFoundError:
            self.library = []
        except json.JSONDecodeError:
            self.library = []

    def save_library(self):
        """Save library data to a file."""
        with open(self.filename, "w") as file:
            json.dump(self.library, file, indent=4)

    def add_book(self, title, author, year, genre, read_status):
        """Add a new book to the library."""
        self.library.append({
            "title": title,
            "author": author,
            "year": year,
            "genre": genre,
            "read": read_status
        })
        self.save_library()
        st.success("🎉 Book added successfully! 📚")

    def remove_book(self, title):
        """Remove a book by title."""
        for book in self.library:
            if book["title"].lower() == title.lower():
                self.library.remove(book)
                self.save_library()
                st.success("🗑️ Book removed successfully! 📖")
                return
        st.error("📚 Book not found! 😞")

    def search_book(self, query):
        """Search for a book by title or author."""
        matches = [book for book in self.library if query in book["title"].lower() or query in book["author"].lower()]
        
        if matches:
            st.subheader("📚 Matching Books:")
            for book in matches:
                status = "Read" if book["read"] else "Unread"
                st.write(f"{book['title']} by {book['author']} ({book['year']}) - {book['genre']} - {status}")
        else:
            st.error("❌ No matching books found.")

    def edit_book(self, title, new_title, new_author, new_year, new_genre, read_status):
        """Edit book details."""
        for book in self.library:
            if book["title"].lower() == title.lower():
                book["title"] = new_title or book["title"]
                book["author"] = new_author or book["author"]
                book["year"] = new_year or book["year"]
                book["genre"] = new_genre or book["genre"]
                book["read"] = read_status
                self.save_library()
                st.success("📚 Book updated successfully! 🎉")
                return
        st.error("❌ Book not found!")

    def display_books(self):
        """Display all books."""
        if not self.library:
            st.warning("📚 No books in library.")
            return
        
        st.subheader("📖 Your Library:")
        for book in self.library:
            status = "Read" if book["read"] else "Unread"
            st.write(f"{book['title']} by {book['author']} ({book['year']}) - {book['genre']} - {status}")

    def display_statistics(self):
        """Show total books and percentage read."""
        total = len(self.library)
        read_books = sum(1 for book in self.library if book["read"])
        percent_read = (read_books / total * 100) if total > 0 else 0
        st.write(f"📊 Total books: {total}")
        st.write(f"📚 Percentage read: {percent_read:.2f}%")

# Streamlit interface
def main():
    manager = PersonalLibraryManager()

    st.title("🌟 Personal Library Manager 🌟")

    menu = ["📚 Add a book", "🗑️ Remove a book", "🔍 Search for a book", "✏️ Edit a book", "📖 Display all books", "📊 Display statistics", "🏁 Exit"]
    choice = st.sidebar.selectbox("Select an action:", menu)

    if choice == "📚 Add a book":
        st.subheader("Add a Book")
        title = st.text_input("📖 Title")
        author = st.text_input("✍️ Author")
        year = st.text_input("📅 Year")
        genre = st.text_input("📚 Genre")
        read_status = st.selectbox("✅ Have you read this book?", ["Yes", "No"]) == "Yes"

        if st.button("Add Book"):
            if title and author and year and genre:
                manager.add_book(title, author, year, genre, read_status)
            else:
                st.error("❌ Please fill in all fields.")

    elif choice == "🗑️ Remove a book":
        st.subheader("Remove a Book")
        title = st.text_input("📖 Enter the title of the book to remove")
        if st.button("Remove Book"):
            if title:
                manager.remove_book(title)
            else:
                st.error("❌ Please enter a book title.")

    elif choice == "🔍 Search for a book":
        st.subheader("Search for a Book")
        query = st.text_input("🔎 Enter title or author to search")
        if st.button("Search"):
            if query:
                manager.search_book(query)
            else:
                st.error("❌ Please enter a search term.")

    elif choice == "✏️ Edit a book":
        st.subheader("Edit a Book")
        title = st.text_input("📖 Enter the title of the book to edit")
        new_title = st.text_input("New Title")
        new_author = st.text_input("New Author")
        new_year = st.text_input("New Year")
        new_genre = st.text_input("New Genre")
        read_status = st.selectbox("✅ Have you read this book?", ["Yes", "No"]) == "Yes"

        if st.button("Edit Book"):
            if title:
                manager.edit_book(title, new_title, new_author, new_year, new_genre, read_status)
            else:
                st.error("❌ Please enter the title of the book to edit.")

    elif choice == "📖 Display all books":
        manager.display_books()

    elif choice == "📊 Display statistics":
        manager.display_statistics()

    elif choice == "🏁 Exit":
        manager.save_library()
        st.info("💾 Library saved to file. Goodbye!")

if __name__ == "__main__":
    main()
