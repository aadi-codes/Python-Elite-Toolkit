import gzip


def compress(file_path, compression_level="medium"):
    try:
        compression_levels = {
            "low": 1,
            "medium": 5,
            "high": 9
        }

        if compression_level not in compression_levels:
            raise ValueError("Invalid compression level")

        compression_level_value = compression_levels[compression_level]

        with open(file_path, 'rb') as file:
            compressed_file_path = file_path + f'_{compression_level}.gz'
            with gzip.open(compressed_file_path, 'wb', compresslevel=compression_level_value) as compressed_file:
                compressed_file.writelines(file)
        return True, compressed_file_path
    except Exception as e:
        return False, str(e)
