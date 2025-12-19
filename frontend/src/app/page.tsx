"use client";

import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Loader2, Copy, Send, Facebook, Instagram, MessageSquare, Image as ImageIcon, Sparkles, BrainCircuit, Globe, Lightbulb } from "lucide-react";
import ReactMarkdown from "react-markdown";
import axios from "axios";
import Link from "next/link";
import { Settings } from "lucide-react";
import { Switch } from "@/components/ui/switch";

export default function Dashboard() {
  const [topic, setTopic] = useState("");
  const [platform, setPlatform] = useState("facebook");
  const [style, setStyle] = useState("專業且親切");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState("");
  const [useAgent, setUseAgent] = useState(false);
  const [useSearch, setUseSearch] = useState(false);
  const [logs, setLogs] = useState<string[]>([]);
  
  // Vision state
  const [imageFile, setImageFile] = useState<File | null>(null);
  const [visionLoading, setVisionLoading] = useState(false);
  const [visionResult, setVisionResult] = useState("");

  // Brainstorm state
  const [idea, setIdea] = useState("");
  const [brainstormResult, setBrainstormResult] = useState("");
  const [brainstormLoading, setBrainstormLoading] = useState(false);

  const [activeTab, setActiveTab] = useState("write");

  const handleGenerate = async () => {
    if (!topic) return;
    setLoading(true);
    setLogs([]);
    try {
      const response = await axios.post("http://localhost:8000/api/copy/generate", {
        platform,
        topic,
        style,
        use_agent: useAgent,
        use_search: useSearch,
      });
      setResult(response.data.content);
      setLogs(response.data.logs || []);
    } catch (error) {
      console.error("Generation failed", error);
      setResult("生成失敗，請檢查後端伺服器是否啟動。");
    } finally {
      setLoading(false);
    }
  };

  const handleVisionAnalyze = async () => {
    if (!imageFile) return;
    setVisionLoading(true);
    const formData = new FormData();
    formData.append("file", imageFile);
    try {
      const response = await axios.post("http://localhost:8000/api/vision/analyze", formData);
      setVisionResult(response.data.analysis);
    } catch (error) {
      console.error("Vision analysis failed", error);
      setVisionResult("圖片分析失敗。");
    } finally {
      setVisionLoading(false);
    }
  };

  const handleBrainstorm = async () => {
    if (!idea) return;
    setBrainstormLoading(true);
    try {
      const response = await axios.post("http://localhost:8000/api/copy/brainstorm", {
        idea,
        platform
      });
      setBrainstormResult(response.data.suggestions);
    } catch (error) {
      console.error("Brainstorming failed", error);
      setBrainstormResult("討論失敗，請稍後再試。");
    } finally {
      setBrainstormLoading(false);
    }
  };

  const handleUseAnalysis = () => {
    if (!visionResult) return;
    setTopic(`基於以下圖片分析結果，撰寫一篇吸引人的貼文：\n\n${visionResult}`);
    setActiveTab("write");
  };

  const handleUseBrainstorm = () => {
    if (!brainstormResult) return;
    setTopic(`基於以下討論出的主題與大綱，撰寫一篇正式貼文：\n\n${brainstormResult}`);
    setActiveTab("write");
  };

  const copyToClipboard = (text: string) => {
    navigator.clipboard.writeText(text);
    alert("已複製到剪貼簿！");
  };

  return (
    <div className="container mx-auto py-10 px-4 max-w-4xl">
      <header className="mb-10 text-center relative">
        <div className="absolute right-0 top-0">
          <Link href="/brand">
            <Button variant="outline" size="sm">
              <Settings className="w-4 h-4 mr-2" />
              品牌設定
            </Button>
          </Link>
        </div>
        <h1 className="text-4xl font-bold tracking-tight mb-2 text-black dark:text-white">AI 社群文案 Agent</h1>
        <p className="text-muted-foreground">為您的 Facebook、Instagram 與 Threads 打造高品質文案</p>
      </header>

      <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full">
        <TabsList className="grid w-full grid-cols-3 mb-8">
          <TabsTrigger value="write">文案生成</TabsTrigger>
          <TabsTrigger value="vision">視覺理解 (AI 看圖)</TabsTrigger>
          <TabsTrigger value="brainstorm">靈感討論 (主題發想)</TabsTrigger>
        </TabsList>

        <TabsContent value="write">
          <div className="grid gap-6 md:grid-cols-2">
            <Card>
              <CardHeader>
                <CardTitle>文案設定</CardTitle>
                <CardDescription>輸入主題並選擇平台風格</CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="space-y-2">
                  <label className="text-sm font-medium">選擇平台</label>
                  <Tabs defaultValue="facebook" onValueChange={setPlatform}>
                    <TabsList className="grid grid-cols-3 w-full">
                      <TabsTrigger value="facebook"><Facebook className="w-4 h-4 mr-2" />FB</TabsTrigger>
                      <TabsTrigger value="instagram"><Instagram className="w-4 h-4 mr-2" />IG</TabsTrigger>
                      <TabsTrigger value="threads"><MessageSquare className="w-4 h-4 mr-2" />Threads</TabsTrigger>
                    </TabsList>
                  </Tabs>
                </div>

                <div className="space-y-2">
                  <label className="text-sm font-medium">貼文主題</label>
                  <Textarea 
                    placeholder="例如：介紹我們新推出的 AI 咖啡機，強調自動化與口感..." 
                    className="h-32"
                    value={topic}
                    onChange={(e) => setTopic(e.target.value)}
                  />
                </div>

                <div className="space-y-2">
                  <label className="text-sm font-medium">語氣風格</label>
                  <Select value={style} onValueChange={setStyle}>
                    <SelectTrigger>
                      <SelectValue placeholder="選擇風格" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="專業且親切">專業且親切</SelectItem>
                      <SelectItem value="幽默風趣">幽默風趣</SelectItem>
                      <SelectItem value="感性動人">感性動人</SelectItem>
                      <SelectItem value="簡潔有力">簡潔有力</SelectItem>
                    </SelectContent>
                  </Select>
                </div>

                <div className="flex items-center justify-between p-3 bg-muted/50 rounded-lg border border-dashed">
                  <div className="flex items-center space-x-2">
                    <BrainCircuit className="w-4 h-4 text-primary" />
                    <div className="space-y-0.5">
                      <label className="text-sm font-medium">多 Agent 協作模式</label>
                      <p className="text-xs text-muted-foreground">引入編輯部流程，提升文案品質</p>
                    </div>
                  </div>
                  <Switch checked={useAgent} onCheckedChange={setUseAgent} />
                </div>

                <div className="flex items-center justify-between p-3 bg-muted/50 rounded-lg border border-dashed">
                  <div className="flex items-center space-x-2">
                    <Globe className="w-4 h-4 text-blue-500" />
                    <div className="space-y-0.5">
                      <label className="text-sm font-medium">聯網搜尋模式</label>
                      <p className="text-xs text-muted-foreground">結合最新時事與趨勢</p>
                    </div>
                  </div>
                  <Switch checked={useSearch} onCheckedChange={setUseSearch} />
                </div>

                <Button 
                  className="w-full" 
                  onClick={handleGenerate} 
                  disabled={loading || !topic}
                >
                  {loading ? <Loader2 className="mr-2 h-4 w-4 animate-spin" /> : <Send className="mr-2 h-4 w-4" />}
                  開始生成
                </Button>
              </CardContent>
            </Card>

            <Card className="flex flex-col">
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <div className="space-y-1">
                  <CardTitle>生成結果</CardTitle>
                  <CardDescription>AI 為您準備的文案</CardDescription>
                </div>
                {result && (
                  <Button variant="outline" size="icon" onClick={() => copyToClipboard(result)}>
                    <Copy className="h-4 w-4" />
                  </Button>
                )}
              </CardHeader>
              <CardContent className="flex-1 overflow-auto space-y-4">
                {logs.length > 0 && (
                  <div className="bg-muted p-3 rounded-md text-xs font-mono space-y-1 border">
                    <p className="text-muted-foreground mb-1 font-bold">思考過程：</p>
                    {logs.map((log, i) => (
                      <div key={i} className="flex items-start">
                        <span className="text-primary mr-2">›</span>
                        <span>{log}</span>
                      </div>
                    ))}
                  </div>
                )}
                
                {result ? (
                  <div className="prose prose-sm dark:prose-invert max-w-none">
                    <ReactMarkdown>{result}</ReactMarkdown>
                  </div>
                ) : (
                  <div className="h-full flex items-center justify-center text-muted-foreground italic">
                    尚未生成內容
                  </div>
                )}
              </CardContent>
            </Card>
          </div>
        </TabsContent>

        <TabsContent value="vision">
          <div className="grid gap-6 md:grid-cols-2">
            <Card>
              <CardHeader>
                <CardTitle>圖片分析</CardTitle>
                <CardDescription>上傳圖片，讓 AI 幫你找靈感</CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="border-2 border-dashed border-muted rounded-lg p-10 text-center">
                  <Input 
                    type="file" 
                    accept="image/*" 
                    className="hidden" 
                    id="image-upload"
                    onChange={(e) => setImageFile(e.target.files?.[0] || null)}
                  />
                  <label htmlFor="image-upload" className="cursor-pointer flex flex-col items-center">
                    <ImageIcon className="w-12 h-12 text-muted-foreground mb-2" />
                    <span className="text-sm text-muted-foreground">
                      {imageFile ? imageFile.name : "點擊或拖曳圖片至此"}
                    </span>
                  </label>
                </div>
                
                <Button 
                  className="w-full" 
                  onClick={handleVisionAnalyze} 
                  disabled={visionLoading || !imageFile}
                >
                  {visionLoading ? <Loader2 className="mr-2 h-4 w-4 animate-spin" /> : <Sparkles className="mr-2 h-4 w-4" />}
                  分析圖片
                </Button>
              </CardContent>
            </Card>

            <Card className="flex flex-col">
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <div className="space-y-1">
                  <CardTitle>分析結果</CardTitle>
                  <CardDescription>圖片的視覺特徵與建議</CardDescription>
                </div>
                <div className="flex gap-2">
                  {visionResult && (
                    <Button variant="default" size="sm" onClick={handleUseAnalysis}>
                      <Send className="w-4 h-4 mr-2" />
                      生成貼文
                    </Button>
                  )}
                  {visionResult && (
                    <Button variant="outline" size="icon" onClick={() => copyToClipboard(visionResult)}>
                      <Copy className="h-4 w-4" />
                    </Button>
                  )}
                </div>
              </CardHeader>
              <CardContent className="flex-1 overflow-auto">
                {visionResult ? (
                  <div className="prose prose-sm dark:prose-invert max-w-none">
                    <ReactMarkdown>{visionResult}</ReactMarkdown>
                  </div>
                ) : (
                  <div className="h-full flex items-center justify-center text-muted-foreground italic">
                    請上傳圖片並點擊分析
                  </div>
                )}
              </CardContent>
            </Card>
          </div>
        </TabsContent>

        <TabsContent value="brainstorm">
          <div className="grid gap-6 md:grid-cols-2">
            <Card>
              <CardHeader>
                <CardTitle>靈感討論</CardTitle>
                <CardDescription>輸入初步想法，讓 AI 幫你發想切入點</CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="space-y-2">
                  <label className="text-sm font-medium">初步想法</label>
                  <Textarea 
                    placeholder="例如：我想推廣一款新的環保杯，但不知道該從什麼角度切入..." 
                    className="h-32"
                    value={idea}
                    onChange={(e) => setIdea(e.target.value)}
                  />
                </div>
                
                <Button 
                  className="w-full" 
                  onClick={handleBrainstorm} 
                  disabled={brainstormLoading || !idea}
                >
                  {brainstormLoading ? <Loader2 className="mr-2 h-4 w-4 animate-spin" /> : <Lightbulb className="mr-2 h-4 w-4" />}
                  開始討論
                </Button>
              </CardContent>
            </Card>

            <Card className="flex flex-col">
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <div className="space-y-1">
                  <CardTitle>討論建議</CardTitle>
                  <CardDescription>AI 提供的創意切入點</CardDescription>
                </div>
                <div className="flex gap-2">
                  {brainstormResult && (
                    <Button variant="default" size="sm" onClick={handleUseBrainstorm}>
                      <Send className="w-4 h-4 mr-2" />
                      採納並寫文案
                    </Button>
                  )}
                  {brainstormResult && (
                    <Button variant="outline" size="icon" onClick={() => copyToClipboard(brainstormResult)}>
                      <Copy className="h-4 w-4" />
                    </Button>
                  )}
                </div>
              </CardHeader>
              <CardContent className="flex-1 overflow-auto">
                {brainstormResult ? (
                  <div className="prose prose-sm dark:prose-invert max-w-none">
                    <ReactMarkdown>{brainstormResult}</ReactMarkdown>
                  </div>
                ) : (
                  <div className="h-full flex items-center justify-center text-muted-foreground italic">
                    請輸入想法並點擊開始討論
                  </div>
                )}
              </CardContent>
            </Card>
          </div>
        </TabsContent>
      </Tabs>
    </div>
  );
}

