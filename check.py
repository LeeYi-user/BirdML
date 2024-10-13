import onnxruntime as ort

# 查看可用的執行提供者（Execution Providers）
providers = ort.get_available_providers()
print(providers)

# 如果有 GPU，應該能看到 CUDA 的提供者
