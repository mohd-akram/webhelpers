:mod:`webhelpers.path`
======================

.. automodule:: webhelpers.path

.. currentmodule:: webhelpers.path

.. autoclass:: Path

   **Constructors:**

   .. automethod:: __new__
   .. automethod:: cwd

   **Properties:**

   **parent**
       The path without the final component; akin to os.path.dirname().
       Example: Path('/usr/lib/libpython.so').parent => Path('/usr/lib')
       

   **name**
       The final component of the path.
       Example: path('/usr/lib/libpython.so').name => Path('libpython.so')

   **stem**
       Same as path.name but with one file extension stripped off.
       Example: path('/home/guido/python.tar.gz').stem => Path('python.tar')

   **ext**
       The file extension, for example '.py'.

   **Absolute paths:**

   .. automethod:: isabsolute

   .. automethod:: absolute

   **Joining paths:**

   .. automethod:: joinpath

   .. automethod:: child

   **Path modification:**

   .. automethod:: ancestor

   .. automethod:: norm
   
   .. automethod:: norm_case

   .. automethod:: expand_user

   .. automethod:: expand_vars

   .. automethod:: expand

   **Calculating paths:**

   .. automethod:: relpath

   .. automethod:: resolve

   .. automethod:: strip_parents

   **File reading and writing:**

   .. automethod:: read_file

   .. automethod:: write_file
