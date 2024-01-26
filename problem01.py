# real NULL action 58
# https://serieson.naver.com/v2/movie/508557
# https://serieson.naver.com/v2/movie/196939
# Traceback (most recent call last):
#   File "C:\Intel_edge\Python_Project\intel_AI\OMG\job01_movie_project.py", line 69, in <module>
#     df_section_titles["text"] = texts
#   File "C:\Intel_edge\Python_Project\intel_AI\OMG\.venv\lib\site-packages\pandas\core\frame.py", line 3950, in __setitem__
#     self._set_item(key, value)
#   File "C:\Intel_edge\Python_Project\intel_AI\OMG\.venv\lib\site-packages\pandas\core\frame.py", line 4143, in _set_item
#     value = self._sanitize_column(value)
#   File "C:\Intel_edge\Python_Project\intel_AI\OMG\.venv\lib\site-packages\pandas\core\frame.py", line 4870, in _sanitize_column
#     com.require_length_match(value, self.index)
#   File "C:\Intel_edge\Python_Project\intel_AI\OMG\.venv\lib\site-packages\pandas\core\common.py", line 576, in require_length_match
#     raise ValueError(
# ValueError: Length of values (60) does not match length of index (61)