// ----------------------------------------------------------------------------
//  ServerlessLLM
//  Copyright (c) ServerlessLLM Team 2024                                       
//                                                                               
//   Licensed under the Apache License, Version 2.0 (the "License");             
//   you may not use this file except in compliance with the License.            
//                                                                               
//   You may obtain a copy of the License at                                     
//                                                                               
//                   http://www.apache.org/licenses/LICENSE-2.0                  
//                                                                               
//   Unless required by applicable law or agreed to in writing, software         
//   distributed under the License is distributed on an "AS IS" BASIS,           
//   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.    
//   See the License for the specific language governing permissions and         
//   limitations under the License.                                              
//  ---------------------------------------------------------------------------- 
#include "gpu_replica.h"

#include <cuda_runtime.h>
#include <glog/logging.h>

void GpuReplica::Clear() {
  for (auto& [device_id, device_ptr] : device_ptrs_) {
    cudaSetDevice(device_id);
    cudaError_t err = cudaIpcCloseMemHandle(device_ptr);
    if (err != cudaSuccess) {
      LOG(ERROR) << "Failed to close memory handle for device " << device_id
                 << " error: " << cudaGetErrorString(err);
    }
  }
  gpu_loading_queue_.clear();
  tensor_offsets_.clear();
  state_ = MemoryState::INTERRUPTED;
  cv_.notify_all();
}