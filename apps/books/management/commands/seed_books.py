"""
Management command to populate the library with sample books.
"""
from django.core.management.base import BaseCommand
from apps.books.models import Book
from datetime import date
import random


class Command(BaseCommand):
    help = 'Populate the library with sample books'

    def handle(self, *args, **options):
        self.stdout.write('📚 Adding sample books to library...\n')

        # Sample books organized by category
        sample_books = {
            'Programming': [
                ('Python Crash Course', 'Eric Matthes', 'A hands-on project-based introduction'),
                ('Fluent Python', 'Luciano Ramalho', 'Clear concise and effective programming'),
                ('Django for Professionals', 'William Vincent', 'Build production-ready web apps'),
                ('Two Scoops of Django', 'Daniel Feldroy', 'Best practices for Django development'),
                ('Effective Python', 'Brett Slatkin', '90 specific ways to write better Python'),
                ('Python Cookbook', 'David Beazley', 'Recipes for mastering Python 3'),
                ('Learning Python', 'Mark Lutz', 'Powerful object-oriented programming'),
                ('Automate the Boring Stuff', 'Al Sweigart', 'Practical programming for beginners'),
                ('Clean Code', 'Robert Martin', 'A handbook of agile software craftsmanship'),
                ('The Pragmatic Programmer', 'David Thomas', 'Your journey to mastery'),
            ],
            'Web Development': [
                ('JavaScript: The Good Parts', 'Douglas Crockford', 'Working with the good parts'),
                ('Eloquent JavaScript', 'Marijn Haverbeke', 'A modern introduction to programming'),
                ('CSS Secrets', 'Lea Verou', 'Better solutions to everyday problems'),
                ('Learning React', 'Alex Banks', 'Modern patterns for developing React apps'),
                ('Vue.js in Action', 'Erik Hanchett', 'Building user interfaces'),
                ('Node.js Design Patterns', 'Mario Casciaro', 'Design and implement production-grade'),
                ('HTML and CSS', 'Jon Duckett', 'Design and build websites'),
                ('Web Design with HTML5', 'Patrick Carey', 'Comprehensive web development'),
                ('PHP and MySQL', 'Luke Welling', 'Web development fundamentals'),
                ('Full Stack Development', 'William Vincent', 'Django REST and React'),
            ],
            'Data Science': [
                ('Hands-On Machine Learning', 'Aurélien Géron', 'Scikit-Learn and TensorFlow'),
                ('Python for Data Analysis', 'Wes McKinney', 'Data wrangling with Pandas'),
                ('Introduction to Statistical Learning', 'Gareth James', 'Applications in R'),
                ('Deep Learning', 'Ian Goodfellow', 'Comprehensive deep learning textbook'),
                ('Data Science from Scratch', 'Joel Grus', 'First principles with Python'),
                ('Pattern Recognition', 'Christopher Bishop', 'Machine learning approaches'),
                ('The Elements of Statistical Learning', 'Trevor Hastie', 'Data mining and prediction'),
                ('Practical Statistics', 'Peter Bruce', 'For data scientists'),
                ('Feature Engineering', 'Alice Zheng', 'For machine learning'),
                ('Natural Language Processing', 'Steven Bird', 'With Python'),
            ],
            'Business': [
                ('Good to Great', 'Jim Collins', 'Why some companies make the leap'),
                ('The Lean Startup', 'Eric Ries', 'How today entrepreneurs use innovation'),
                ('Zero to One', 'Peter Thiel', 'Notes on startups'),
                ('Start with Why', 'Simon Sinek', 'How great leaders inspire action'),
                ('The Hard Thing About Hard Things', 'Ben Horowitz', 'Building a business'),
                ('Blue Ocean Strategy', 'W. Chan Kim', 'How to create uncontested market space'),
                ('Built to Last', 'Jim Collins', 'Successful habits of visionary companies'),
                ('The Innovator Dilemma', 'Clayton Christensen', 'When new technologies cause failure'),
                ('Thinking, Fast and Slow', 'Daniel Kahneman', 'Two systems that drive thinking'),
                ('Principles', 'Ray Dalio', 'Life and work'),
            ],
            'Classic Literature': [
                ('War and Peace', 'Leo Tolstoy', 'A novel about Russian society'),
                ('Anna Karenina', 'Leo Tolstoy', 'Tragedy of Russian aristocrat'),
                ('Crime and Punishment', 'Fyodor Dostoevsky', 'Psychological exploration of crime'),
                ('The Brothers Karamazov', 'Fyodor Dostoevsky', 'Philosophical debate about God'),
                ('Don Quixote', 'Miguel de Cervantes', 'Adventures of a would-be knight'),
                ('Moby Dick', 'Herman Melville', 'The pursuit of a great white whale'),
                ('Great Expectations', 'Charles Dickens', 'A story of aspiration and morality'),
                ('A Tale of Two Cities', 'Charles Dickens', 'London and Paris during revolution'),
                ('Middlemarch', 'George Eliot', 'Study of provincial life'),
                ('The Count of Monte Cristo', 'Alexandre Dumas', 'Adventure tale of revenge'),
            ],
            'Modern Fiction': [
                ('The Road', 'Cormac McCarthy', 'A father and son journey'),
                ('Life of Pi', 'Yann Martel', 'A boy stranded at sea'),
                ('The Kite Runner', 'Khaled Hosseini', 'Story of friendship and redemption'),
                ('A Thousand Splendid Suns', 'Khaled Hosseini', 'Two women in Afghanistan'),
                ('The Shadow of the Wind', 'Carlos Ruiz Zafón', 'A mystery in Barcelona'),
                ('Cloud Atlas', 'David Mitchell', 'Six interconnected stories'),
                ('Atonement', 'Ian McEwan', 'A crime and its aftermath'),
                ('Never Let Me Go', 'Kazuo Ishiguro', 'A dystopian novel about clones'),
                ('The Goldfinch', 'Donna Tartt', 'A boy and a famous painting'),
                ('All the Light We Cannot See', 'Anthony Doerr', 'WWII Paris and Germany'),
            ],
            'Science': [
                ('A Brief History of Time', 'Stephen Hawking', 'From big bang to black holes'),
                ('The Selfish Gene', 'Richard Dawkins', 'Popular science about evolution'),
                ('Cosmos', 'Carl Sagan', 'A personal voyage'),
                ('The Origin of Species', 'Charles Darwin', 'Natural selection theory'),
                ('Silent Spring', 'Rachel Carson', 'Environmental pollution'),
                ('The Double Helix', 'James Watson', 'Discovery of DNA structure'),
                ('Surely You re Joking Mr Feynman', 'Richard Feynman', 'Adventures of a physicist'),
                ('The Elegant Universe', 'Brian Greene', 'String theory and dimensions'),
                ('The Gene', 'Siddhartha Mukherjee', 'An intimate history'),
                ('Sapiens', 'Yuval Noah Harari', 'Brief history of humankind'),
            ],
            'Self-Development': [
                ('The 7 Habits', 'Stephen Covey', 'Highly effective people'),
                ('How to Win Friends', 'Dale Carnegie', 'Influence people'),
                ('Atomic Habits', 'James Clear', 'Tiny changes remarkable results'),
                ('The Power of Habit', 'Charles Duhigg', 'Why we do what we do'),
                ('Mindset', 'Carol Dweck', 'The new psychology of success'),
                ('Grit', 'Angela Duckworth', 'Power of passion and perseverance'),
                ('The Subtle Art', 'Mark Manson', 'A counterintuitive approach'),
                ('Deep Work', 'Cal Newport', 'Rules for focused success'),
                ('Thinking Fast and Slow', 'Daniel Kahneman', 'Two thinking systems'),
                ('Outliers', 'Malcolm Gladwell', 'The story of success'),
            ],
            'History': [
                ('Guns Germs and Steel', 'Jared Diamond', 'Fates of human societies'),
                ('A People History', 'Howard Zinn', 'History of the United States'),
                ('The Rise and Fall', 'William Shirer', 'Third Reich history'),
                ('Enlightenment Now', 'Steven Pinker', 'The case for reason and science'),
                ('Team of Rivals', 'Doris Kearns Goodwin', 'Lincoln political genius'),
                ('The Silk Roads', 'Peter Frankopan', 'A new history of the world'),
                ('SPQR', 'Mary Beard', 'A history of ancient Rome'),
                ('The Wright Brothers', 'David McCullough', 'Story of aviation pioneers'),
                ('1776', 'David McCullough', 'America in the year of revolution'),
                ('The Warmth of Other Suns', 'Isabel Wilkerson', 'Great Migration'),
            ],
            'Philosophy': [
                ('Meditations', 'Marcus Aurelius', 'Stoic philosophy wisdom'),
                ('The Republic', 'Plato', 'Socratic dialogue about justice'),
                ('Nicomachean Ethics', 'Aristotle', 'On virtue and happiness'),
                ('Beyond Good and Evil', 'Friedrich Nietzsche', 'Future of philosophy'),
                ('Being and Time', 'Martin Heidegger', 'Existential phenomenology'),
                ('The Art of War', 'Sun Tzu', 'Ancient Chinese military text'),
                ('Thus Spoke Zarathustra', 'Friedrich Nietzsche', 'Philosophical novel'),
                ('Critique of Pure Reason', 'Immanuel Kant', 'Epistemology and metaphysics'),
                ('The Prince', 'Niccolò Machiavelli', 'Political philosophy'),
                ('Tao Te Ching', 'Lao Tzu', 'Fundamental text of Taoism'),
            ],
        }

        created_count = 0
        book_num = 1
        total_books = sum(len(books) for books in sample_books.values())

        for category, books in sample_books.items():
            for title, author, description in books:
                # Generate unique ISBN
                isbn = f'978{random.randint(1000000000, 9999999999)}'
                page_count = random.randint(150, 700)
                year = random.randint(1980, 2024)
                month = random.randint(1, 12)
                day = random.randint(1, 28)

                book, created = Book.objects.get_or_create(
                    title=title,
                    author=author,
                    defaults={
                        'isbn': isbn,
                        'description': description,
                        'page_count': page_count,
                        'genre': category,
                        'published_date': date(year, month, day),
                        'is_available': True,
                    }
                )

                if created:
                    created_count += 1
                    self.stdout.write(f'  ✓ Added: {title}')
                else:
                    self.stdout.write(f'  - Exists: {title}')

                book_num += 1

        self.stdout.write(self.style.SUCCESS(
            f'\\n✓ Library populated with {created_count} new books ({total_books} total in catalog).'
        ))
