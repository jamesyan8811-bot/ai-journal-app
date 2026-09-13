export type NavItem = { to: string; label: string; code: string };

export const navItems: NavItem[] = [
  { to: "/", label: "Overview", code: "00" },
  { to: "/recommender", label: "Video Recommender", code: "01" },
  { to: "/sessions", label: "Sessions", code: "02" },
  { to: "/channels", label: "Discussion Channels", code: "03" },
  { to: "/brain", label: "AI Brain Lab", code: "04" },
  { to: "/portfolio", label: "Portfolio Notes", code: "05" },
];

export const stats = [
  { label: "Videos", value: 12 },
  { label: "Tutorial sessions", value: 8 },
  { label: "Discussion posts", value: 6 },
  { label: "Sample members", value: 6 },
];

export type Member = {
  id: string;
  name: string;
  grade: number;
  topics: string[];
  level: "Beginner" | "Intermediate" | "Advanced";
  budgetMin: number;
  watched: string[];
};

export const members: Member[] = [
  { id: "U001", name: "Avery", grade: 9, topics: ["AI Agents", "Generative AI", "Prompting"], level: "Beginner", budgetMin: 30, watched: ["V03"] },
  { id: "U002", name: "Ben", grade: 10, topics: ["Deep Learning", "Multimodal AI"], level: "Intermediate", budgetMin: 45, watched: ["V01", "V05"] },
  { id: "U003", name: "Carlos", grade: 11, topics: ["Robotics", "Reinforcement Learning"], level: "Intermediate", budgetMin: 60, watched: [] },
  { id: "U004", name: "Divya", grade: 12, topics: ["Retrieval-Augmented Generation", "Prompting"], level: "Advanced", budgetMin: 45, watched: ["V02"] },
  { id: "U005", name: "Ethan", grade: 9, topics: ["Robotics", "Machine Learning"], level: "Beginner", budgetMin: 20, watched: [] },
  { id: "U006", name: "Fatima", grade: 10, topics: ["Multimodal AI", "Generative AI"], level: "Beginner", budgetMin: 30, watched: ["V04"] },
];

export type Video = {
  id: string;
  title: string;
  desc: string;
  topic: string;
  level: "Beginner" | "Intermediate" | "Advanced";
  minutes: number;
  score: number;
};

export const videos: Video[] = [
  { id: "V01", title: "Prompt Engineering and AI Evaluation", desc: "Shows how prompts guide AI systems and why outputs should be tested carefully.", topic: "Prompting", level: "Beginner", minutes: 9, score: 0.54 },
  { id: "V02", title: "Multimodal AI: Models That See, Hear and Read", desc: "Explains models that combine text, images, audio, and video to understand the world.", topic: "Multimodal AI", level: "Beginner", minutes: 11, score: 0.37 },
  { id: "V03", title: "Autonomous AI Agents 101", desc: "A gentle intro to agents that plan, use tools, and take actions on your behalf.", topic: "AI Agents", level: "Beginner", minutes: 8, score: 0.33 },
  { id: "V04", title: "Generative Models Under the Hood", desc: "Peek at how diffusion and transformer models actually produce novel content.", topic: "Generative AI", level: "Intermediate", minutes: 14, score: 0.29 },
  { id: "V05", title: "How Reinforcement Learning Teaches Robots", desc: "From reward signals to real motion — how RL loops shape robot behavior.", topic: "Reinforcement Learning", level: "Intermediate", minutes: 12, score: 0.22 },
  { id: "V06", title: "Neural Networks Explained Visually", desc: "Weights, activations, and gradient descent — with clean visual intuitions.", topic: "Deep Learning", level: "Beginner", minutes: 10, score: 0.19 },
];

export type Session = {
  id: string;
  title: string;
  desc: string;
  date: string;
  topic: string;
  difficulty: "Beginner" | "Intermediate" | "Advanced";
  teacher: string;
  capacity: number;
};

export const sessions: Session[] = [
  { id: "S01", title: "Build a Mini Recommender in Python", desc: "Hands-on tutorial: use survey data and content tags to recommend videos.", date: "2026-07-12", topic: "Machine Learning", difficulty: "Beginner", teacher: "James", capacity: 30 },
  { id: "S02", title: "How Neural Networks Learn", desc: "Visual demo of layers, weights, activation, loss, and gradient descent.", date: "2026-07-19", topic: "Deep Learning", difficulty: "Beginner", teacher: "James", capacity: 25 },
  { id: "S03", title: "RAG Workshop: Give Your AI a Library", desc: "Build a tiny retrieval system over club notes and article summaries.", date: "2026-07-26", topic: "Retrieval-Augmented Generation", difficulty: "Intermediate", teacher: "James", capacity: 20 },
  { id: "S04", title: "Prompting Like a Pro", desc: "Structure prompts, chain steps, and evaluate outputs with rubrics.", date: "2026-08-02", topic: "Prompting", difficulty: "Beginner", teacher: "Guest: Ana", capacity: 30 },
  { id: "S05", title: "Agents That Take Actions", desc: "Design agent loops with tools, memory, and safety checks.", date: "2026-08-09", topic: "AI Agents", difficulty: "Intermediate", teacher: "James", capacity: 20 },
  { id: "S06", title: "Multimodal Show & Tell", desc: "Compare captions across models and discuss failure cases.", date: "2026-08-16", topic: "Multimodal AI", difficulty: "Beginner", teacher: "Guest: Rio", capacity: 25 },
  { id: "S07", title: "Robotics Sim Sprint", desc: "Train a virtual robot in a sandbox before it meets the real world.", date: "2026-08-23", topic: "Robotics", difficulty: "Advanced", teacher: "James", capacity: 15 },
  { id: "S08", title: "Responsible AI Roundtable", desc: "Bias, privacy, and what teens should demand from AI tools.", date: "2026-08-30", topic: "Ethics", difficulty: "Beginner", teacher: "James", capacity: 30 },
];

export type Post = {
  channel: string;
  topic: string;
  author: string;
  date: string;
  upvotes: number;
  body: string;
};

export const posts: Post[] = [
  { channel: "multimodal", topic: "Multimodal AI", author: "Fatima", date: "2026-07-05 10:00", upvotes: 10, body: "I want a session where we compare image captions from different models." },
  { channel: "robotics", topic: "Robotics", author: "Ethan", date: "2026-07-04 19:10", upvotes: 7, body: "Can reinforcement learning train a robot in simulation before it tries the real world?" },
  { channel: "rag-and-tools", topic: "Retrieval-Augmented Generation", author: "Divya", date: "2026-07-04 11:30", upvotes: 18, body: "RAG feels like giving the AI a school library card before it answers." },
  { channel: "deep-learning", topic: "Deep Learning", author: "Carlos", date: "2026-07-03 14:45", upvotes: 9, body: "The attention analogy helped me finally understand why transformers can handle long text." },
  { channel: "prompting", topic: "Prompting", author: "Avery", date: "2026-07-02 09:12", upvotes: 12, body: "Rubric-based prompting made my science writeup way clearer." },
  { channel: "agents", topic: "AI Agents", author: "Ben", date: "2026-07-01 16:20", upvotes: 6, body: "What guardrails should a study-buddy agent have before we let it plan our week?" },
];

export const brainTopics: Record<string, string> = {
  "AI Agents": "Autonomous agents plan a goal, pick tools, and take steps — like a study buddy that opens tabs, drafts notes, then checks itself before submitting.",
  "Generative AI": "Models that create new text, images, audio, or code by learning patterns from huge datasets. Think of it as a very fast improviser trained on the internet.",
  "Prompting": "The art of writing clear instructions to an AI. Good prompts = clear role + clear task + examples + a rubric to grade the answer.",
  "Multimodal AI": "Models that mix text, images, audio, and video together. Great for describing a photo, reading a chart, or captioning a lecture clip.",
  "Retrieval-Augmented Generation": "Give the AI a searchable library first, then let it answer. Reduces hallucinations because it can quote real sources.",
  "Deep Learning": "Layered neural nets that learn by adjusting millions of weights via gradient descent. More layers = more abstract patterns.",
  "Reinforcement Learning": "Learn by trial-and-error using rewards. Perfect for robots, games, and any task where you know the goal but not the exact steps.",
  "Robotics": "Combining perception (cameras), planning (AI), and control (motors) so machines can act in the physical world.",
};

export const feedbackWeights = [
  { topic: "Prompting", weight: 0.42 },
  { topic: "Multimodal AI", weight: 0.31 },
  { topic: "AI Agents", weight: 0.28 },
  { topic: "Generative AI", weight: 0.22 },
  { topic: "Deep Learning", weight: 0.15 },
  { topic: "Robotics", weight: 0.09 },
];