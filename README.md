Starting ingestion process...
Connecting to Milvus Lite at: ./milvus_arabic_books.db
/workspace/arabic_rag_api/venv/lib/python3.12/site-packages/milvus_lite/__init__.py:15: UserWarning: pkg_resources is deprecated as an API. See https://setuptools.pypa.io/en/latest/pkg_resources.html. The pkg_resources package is slated for removal as early as 2025-11-30. Refrain from using this package or pin to Setuptools<81.
  from pkg_resources import DistributionNotFound, get_distribution
Creating collection 'arabic_books'...
Collection created.
Loading sentence transformer model: 'intfloat/multilingual-e5-large'
No sentence-transformers model found with name intfloat/multilingual-e5-large. Creating a new one with mean pooling.
Traceback (most recent call last):
  File "/workspace/arabic_rag_api/venv/lib/python3.12/site-packages/huggingface_hub/file_download.py", line 399, in http_get
    import hf_transfer  # type: ignore[no-redef]
    ^^^^^^^^^^^^^^^^^^
ModuleNotFoundError: No module named 'hf_transfer'

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/workspace/arabic_rag_api/venv/lib/python3.12/site-packages/transformers/configuration_utils.py", line 721, in _get_config_dict
    resolved_config_file = cached_file(
                           ^^^^^^^^^^^^
  File "/workspace/arabic_rag_api/venv/lib/python3.12/site-packages/transformers/utils/hub.py", line 322, in cached_file
    file = cached_files(path_or_repo_id=path_or_repo_id, filenames=[filename], **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/workspace/arabic_rag_api/venv/lib/python3.12/site-packages/transformers/utils/hub.py", line 567, in cached_files
    raise e
  File "/workspace/arabic_rag_api/venv/lib/python3.12/site-packages/transformers/utils/hub.py", line 479, in cached_files
    hf_hub_download(
  File "/workspace/arabic_rag_api/venv/lib/python3.12/site-packages/huggingface_hub/utils/_validators.py", line 114, in _inner_fn
    return fn(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^
  File "/workspace/arabic_rag_api/venv/lib/python3.12/site-packages/huggingface_hub/file_download.py", line 1007, in hf_hub_download
    return _hf_hub_download_to_cache_dir(
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/workspace/arabic_rag_api/venv/lib/python3.12/site-packages/huggingface_hub/file_download.py", line 1168, in _hf_hub_download_to_cache_dir
    _download_to_tmp_and_move(
  File "/workspace/arabic_rag_api/venv/lib/python3.12/site-packages/huggingface_hub/file_download.py", line 1735, in _download_to_tmp_and_move
    http_get(
  File "/workspace/arabic_rag_api/venv/lib/python3.12/site-packages/huggingface_hub/file_download.py", line 401, in http_get
    raise ValueError(
ValueError: Fast download using 'hf_transfer' is enabled (HF_HUB_ENABLE_HF_TRANSFER=1) but 'hf_transfer' package is not available in your environment. Try `pip install hf_transfer`.

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/workspace/arabic_rag_api/ingest.py", line 104, in <module>
    main()
  File "/workspace/arabic_rag_api/ingest.py", line 50, in main
    model = SentenceTransformer(_MODEL_NAME, trust_remote_code=True)
            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/workspace/arabic_rag_api/venv/lib/python3.12/site-packages/sentence_transformers/SentenceTransformer.py", line 339, in __init__
    modules = self._load_auto_model(
              ^^^^^^^^^^^^^^^^^^^^^^
  File "/workspace/arabic_rag_api/venv/lib/python3.12/site-packages/sentence_transformers/SentenceTransformer.py", line 2112, in _load_auto_model
    transformer_model = Transformer(
                        ^^^^^^^^^^^^
  File "/workspace/arabic_rag_api/venv/lib/python3.12/site-packages/sentence_transformers/models/Transformer.py", line 87, in __init__
    config, is_peft_model = self._load_config(model_name_or_path, cache_dir, backend, config_args)
                            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/workspace/arabic_rag_api/venv/lib/python3.12/site-packages/sentence_transformers/models/Transformer.py", line 162, in _load_config
    return AutoConfig.from_pretrained(model_name_or_path, **config_args, cache_dir=cache_dir), False
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/workspace/arabic_rag_api/venv/lib/python3.12/site-packages/transformers/models/auto/configuration_auto.py", line 1332, in from_pretrained
    config_dict, unused_kwargs = PretrainedConfig.get_config_dict(pretrained_model_name_or_path, **kwargs)
                                 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/workspace/arabic_rag_api/venv/lib/python3.12/site-packages/transformers/configuration_utils.py", line 662, in get_config_dict
    config_dict, kwargs = cls._get_config_dict(pretrained_model_name_or_path, **kwargs)
                          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/workspace/arabic_rag_api/venv/lib/python3.12/site-packages/transformers/configuration_utils.py", line 744, in _get_config_dict
    raise OSError(
OSError: Can't load the configuration of 'intfloat/multilingual-e5-large'. If you were trying to load it from 'https://huggingface.co/models', make sure you don't have a local directory with the same name. Otherwise, make sure 'intfloat/multilingual-e5-large' is the correct path to a directory containing a config.json file
$ cd /workspace/arabic_rag_api && source venv/bin/activate && unset HF_HUB_ENABLE_HF_TRANSFER && python ingest.py 2>&1 | head -300
t], <DataNotMatchException: (code=1, message=The Input data type is inconsistent with defined schema, {embedding} field should be a FLOAT_VECTOR, but got a {<class 'str'>} instead. Detail: must be real number, not str)>, <Time:{'RPC start': '2025-11-07 10:26:39.290987', 'RPC error': '2025-11-07 10:26:39.295335'}> (decorators.py:253)
    - ERROR processing file manhaj2030_books_cleaned_v1/hadith_sources_cleaned/abudaud.txt: <DataNotMatchException: (code=1, message=The Input data type is inconsistent with defined schema, {embedding} field should be a FLOAT_VECTOR, but got a {<class 'str'>} instead. Detail: must be real number, not str)>
2025-11-07 10:27:26,844 [ERROR][handler]: RPC error: [batch_insert], <DataNotMatchException: (code=1, message=The Input data type is inconsistent with defined schema, {embedding} field should be a FLOAT_VECTOR, but got a {<class 'str'>} instead. Detail: must be real number, not str)>, <Time:{'RPC start': '2025-11-07 10:27:26.841943', 'RPC error': '2025-11-07 10:27:26.844137'}> (decorators.py:253)
    - ERROR processing file manhaj2030_books_cleaned_v1/hadith_sources_cleaned/sahih_ibn_khuzaimah.txt: <DataNotMatchException: (code=1, message=The Input data type is inconsistent with defined schema, {embedding} field should be a FLOAT_VECTOR, but got a {<class 'str'>} instead. Detail: must be real number, not str)>
2025-11-07 10:28:52,665 [ERROR][handler]: RPC error: [batch_insert], <DataNotMatchException: (code=1, message=The Input data type is inconsistent with defined schema, {embedding} field should be a FLOAT_VECTOR, but got a {<class 'str'>} instead. Detail: must be real number, not str)>, <Time:{'RPC start': '2025-11-07 10:28:52.661319', 'RPC error': '2025-11-07 10:28:52.665539'}> (decorators.py:253)
    - ERROR processing file manhaj2030_books_cleaned_v1/hadith_sources_cleaned/muslim.txt: <DataNotMatchException: (code=1, message=The Input data type is inconsistent with defined schema, {embedding} field should be a FLOAT_VECTOR, but got a {<class 'str'>} instead. Detail: must be real number, not str)>
2025-11-07 10:38:43,255 [ERROR][handler]: RPC error: [batch_insert], <DataNotMatchException: (code=1, message=The Input data type is inconsistent with defined schema, {embedding} field should be a FLOAT_VECTOR, but got a {<class 'str'>} instead. Detail: must be real number, not str)>, <Time:{'RPC start': '2025-11-07 10:38:43.233365', 'RPC error': '2025-11-07 10:38:43.255954'}> (decorators.py:253)
    - ERROR processing file manhaj2030_books_cleaned_v1/hadith_sources_cleaned/musnad_ahmad.txt: <DataNotMatchException: (code=1, message=The Input data type is inconsistent with defined schema, {embedding} field should be a FLOAT_VECTOR, but got a {<class 'str'>} instead. Detail: must be real number, not str)>
2025-11-07 10:40:07,040 [ERROR][handler]: RPC error: [batch_insert], <DataNotMatchException: (code=1, message=The Input data type is inconsistent with defined schema, {embedding} field should be a FLOAT_VECTOR, but got a {<class 'str'>} instead. Detail: must be real number, not str)>, <Time:{'RPC start': '2025-11-07 10:40:07.036342', 'RPC error': '2025-11-07 10:40:07.039967'}> (decorators.py:253)
    - ERROR processing file manhaj2030_books_cleaned_v1/hadith_sources_cleaned/ibnmajah.txt: <DataNotMatchException: (code=1, message=The Input data type is inconsistent with defined schema, {embedding} field should be a FLOAT_VECTOR, but got a {<class 'str'>} instead. Detail: must be real number, not str)>
2025-11-07 10:44:01,019 [ERROR][handler]: RPC error: [batch_insert], <DataNotMatchException: (code=1, message=The Input data type is inconsistent with defined schema, {embedding} field should be a FLOAT_VECTOR, but got a {<class 'str'>} instead. Detail: must be real number, not str)>, <Time:{'RPC start': '2025-11-07 10:44:01.008308', 'RPC error': '2025-11-07 10:44:01.019843'}> (decorators.py:253)
    - ERROR processing file manhaj2030_books_cleaned_v1/hadith_sources_cleaned/mujam_kabeer_tabari.txt: <DataNotMatchException: (code=1, message=The Input data type is inconsistent with defined schema, {embedding} field should be a FLOAT_VECTOR, but got a {<class 'str'>} instead. Detail: must be real number, not str)>
2025-11-07 10:44:31,026 [ERROR][handler]: RPC error: [batch_insert], <DataNotMatchException: (code=1, message=The Input data type is inconsistent with defined schema, {embedding} field should be a FLOAT_VECTOR, but got a {<class 'str'>} instead. Detail: must be real number, not str)>, <Time:{'RPC start': '2025-11-07 10:44:31.025245', 'RPC error': '2025-11-07 10:44:31.026894'}> (decorators.py:253)
    - ERROR processing file manhaj2030_books_cleaned_v1/hadith_sources_cleaned/sunan_darimi.txt: <DataNotMatchException: (code=1, message=The Input data type is inconsistent with defined schema, {embedding} field should be a FLOAT_VECTOR, but got a {<class 'str'>} instead. Detail: must be real number, not str)>
2025-11-07 10:45:15,285 [ERROR][handler]: RPC error: [batch_insert], <DataNotMatchException: (code=1, message=The Input data type is inconsistent with defined schema, {embedding} field should be a FLOAT_VECTOR, but got a {<class 'str'>} instead. Detail: must be real number, not str)>, <Time:{'RPC start': '2025-11-07 10:45:15.283141', 'RPC error': '2025-11-07 10:45:15.285491'}> (decorators.py:253)
    - ERROR processing file manhaj2030_books_cleaned_v1/hadith_sources_cleaned/muwatta.txt: <DataNotMatchException: (code=1, message=The Input data type is inconsistent with defined schema, {embedding} field should be a FLOAT_VECTOR, but got a {<class 'str'>} instead. Detail: must be real number, not str)>
2025-11-07 10:47:22,470 [ERROR][handler]: RPC error: [batch_insert], <DataNotMatchException: (code=1, message=The Input data type is inconsistent with defined schema, {embedding} field should be a FLOAT_VECTOR, but got a {<class 'str'>} instead. Detail: must be real number, not str)>, <Time:{'RPC start': '2025-11-07 10:47:22.464952', 'RPC error': '2025-11-07 10:47:22.470849'}> (decorators.py:253)
    - ERROR processing file manhaj2030_books_cleaned_v1/hadith_sources_cleaned/bukhari.txt: <DataNotMatchException: (code=1, message=The Input data type is inconsistent with defined schema, {embedding} field should be a FLOAT_VECTOR, but got a {<class 'str'>} instead. Detail: must be real number, not str)>
2025-11-07 10:49:33,260 [ERROR][handler]: RPC error: [batch_insert], <DataNotMatchException: (code=1, message=The Input data type is inconsistent with defined schema, {embedding} field should be a FLOAT_VECTOR, but got a {<class 'str'>} instead. Detail: must be real number, not str)>, <Time:{'RPC start': '2025-11-07 10:49:33.251795', 'RPC error': '2025-11-07 10:49:33.260811'}> (decorators.py:253)
    - ERROR processing file manhaj2030_books_cleaned_v1/hadith_sources_cleaned/mustadrak_alhakim.txt: <DataNotMatchException: (code=1, message=The Input data type is inconsistent with defined schema, {embedding} field should be a FLOAT_VECTOR, but got a {<class 'str'>} instead. Detail: must be real number, not str)>
2025-11-07 10:54:40,547 [ERROR][handler]: RPC error: [batch_insert], <DataNotMatchException: (code=1, message=The Input data type is inconsistent with defined schema, {embedding} field should be a FLOAT_VECTOR, but got a {<class 'str'>} instead. Detail: must be real number, not str)>, <Time:{'RPC start': '2025-11-07 10:54:40.532014', 'RPC error': '2025-11-07 10:54:40.546967'}> (decorators.py:253)
    - ERROR processing file manhaj2030_books_cleaned_v1/hadith_sources_cleaned/sunan_kubra_bayhaqi.txt: <DataNotMatchException: (code=1, message=The Input data type is inconsistent with defined schema, {embedding} field should be a FLOAT_VECTOR, but got a {<class 'str'>} instead. Detail: must be real number, not str)>
2025-11-07 10:56:39,931 [ERROR][handler]: RPC error: [batch_insert], <DataNotMatchException: (code=1, message=The Input data type is inconsistent with defined schema, {embedding} field should be a FLOAT_VECTOR, but got a {<class 'str'>} instead. Detail: must be real number, not str)>, <Time:{'RPC start': '2025-11-07 10:56:39.925537', 'RPC error': '2025-11-07 10:56:39.931058'}> (decorators.py:253)
    - ERROR p
