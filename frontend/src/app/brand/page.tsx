"use client";

import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Loader2, Upload, CheckCircle, FileText } from "lucide-react";
import axios from "axios";
import Link from "next/link";

export default function BrandSettings() {
  const [file, setFile] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("");

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files) {
      setFile(e.target.files[0]);
    }
  };

  const handleUpload = async () => {
    if (!file) return;
    setLoading(true);
    setMessage("");
    
    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await axios.post("http://localhost:8000/api/brand/upload-brand-info", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });
      setMessage(response.data.message);
      setFile(null);
    } catch (error) {
      console.error("Upload failed", error);
      setMessage("上傳失敗，請檢查後端伺服器。");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container mx-auto py-10 px-4 max-w-2xl">
      <header className="mb-10 text-center">
        <h1 className="text-4xl font-bold tracking-tight mb-2">品牌大腦設定</h1>
        <p className="text-muted-foreground">上傳品牌手冊、過往貼文或風格指南，讓 AI 更懂你的品牌</p>
        <div className="mt-4">
          <Link href="/" className="text-primary hover:underline">← 返回儀表板</Link>
        </div>
      </header>

      <Card>
        <CardHeader>
          <CardTitle>上傳知識庫</CardTitle>
          <CardDescription>支援 PDF, TXT, CSV 格式</CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="grid w-full max-w-sm items-center gap-1.5">
            <Input 
              id="brand-file" 
              type="file" 
              accept=".pdf,.txt,.csv" 
              onChange={handleFileChange}
            />
          </div>
          
          {file && (
            <div className="flex items-center p-2 bg-muted rounded-md">
              <FileText className="w-4 h-4 mr-2 text-primary" />
              <span className="text-sm truncate">{file.name}</span>
            </div>
          )}

          <Button 
            className="w-full" 
            onClick={handleUpload} 
            disabled={loading || !file}
          >
            {loading ? <Loader2 className="mr-2 h-4 w-4 animate-spin" /> : <Upload className="mr-2 h-4 w-4" />}
            上傳並訓練
          </Button>

          {message && (
            <div className="flex items-center justify-center p-3 bg-green-50 text-green-700 rounded-md text-sm">
              <CheckCircle className="w-4 h-4 mr-2" />
              {message}
            </div>
          )}
        </CardContent>
      </Card>

      <div className="mt-10">
        <h3 className="text-lg font-semibold mb-4">為什麼要設定品牌大腦？</h3>
        <ul className="list-disc list-inside space-y-2 text-muted-foreground text-sm">
          <li><strong>一致性：</strong> 確保所有平台的文案語氣統一。</li>
          <li><strong>精準度：</strong> AI 能引用正確的產品資訊與品牌價值。</li>
          <li><strong>效率：</strong> 減少人工修改 AI 初稿的時間。</li>
        </ul>
      </div>
    </div>
  );
}
