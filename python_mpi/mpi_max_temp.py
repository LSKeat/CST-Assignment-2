from mpi4py import MPI
import os
import time
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

def map_reduce(input_data):
    # Enhanced mapper with logging
    year_temp_map = {}
    try:
        for line in input_data:
            tokens = line.split()
            if len(tokens) >= 2:
                year = tokens[0]
                try:
                    temperature = int(tokens[1].strip())
                    year_temp_map[year] = max(year_temp_map.get(year, temperature), temperature)
                except ValueError:
                    logging.warning(f"Invalid temperature value: {tokens[1]}")
    except Exception as e:
        logging.error(f"Error in map_reduce: {e}")
    
    return year_temp_map

def mpi_map_reduce(input_file, output_file):
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()

    logging.info(f"Process {rank} starting")
    start_time = time.time()

    try:
        input_file = os.path.join('/app', input_file)
        output_file = os.path.join(output_file)

        with open(input_file, 'r') as file:
            lines = file.readlines()

        chunk_size = len(lines) // size
        start_idx = rank * chunk_size
        end_idx = (rank + 1) * chunk_size if rank != size - 1 else len(lines)

        chunk_data = lines[start_idx:end_idx]
        local_map = map_reduce(chunk_data)

        all_maps = comm.gather(local_map, root=0)

        if rank == 0:
            final_map = {}
            for map_part in all_maps:
                for year, temp in map_part.items():
                    final_map[year] = max(final_map.get(year, temp), temp)

            with open(output_file, 'w') as output:
                for year, temp in sorted(final_map.items()):
                    output.write(f"{year} {temp}\n")

            end_time = time.time()
            logging.info(f"Execution time: {end_time - start_time} seconds")

    except Exception as e:
        logging.error(f"Error in MPI processing: {e}")
    finally:
        MPI.Finalize()

if __name__ == "__main__":
    input_file = "input_data.txt"
    output_file = f"output_data_{MPI.COMM_WORLD.Get_rank()}.txt"
    mpi_map_reduce(input_file, output_file)