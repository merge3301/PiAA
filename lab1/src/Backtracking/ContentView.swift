import SwiftUI

struct ContentView: View {
    @StateObject private var viewModel = ViewModel()
    private let tableSize: CGFloat = 600
    private let gridSizeRange = 2...40
    
    var body: some View {
        HStack {
            VStack {
                GridSetter()
                Table()
            }
            .padding()
            Divider()
            
            ListSquares()
                .padding()
        }
    }
    
    private func GridSetter() -> some View {
        VStack {
            HStack {
                TextField("Enter grid size", value: $viewModel.gridSize, format: .number)
                    .frame(width: 150)
                    .textFieldStyle(.roundedBorder)
                    .onChange(of: viewModel.gridSize) { oldValue, newValue in
                        viewModel.incorrectGrid = !gridSizeRange.contains(viewModel.gridSize)
                    }
                Stepper("", value: $viewModel.gridSize, in: gridSizeRange)
                Button("Place squares") {
                    withAnimation(.easeIn(duration: 0.5)) {
                        viewModel.placeSqures(tableSize)
                    }
                }
                .disabled(viewModel.incorrectGrid)
            }
        
            if viewModel.incorrectGrid {
                Text("Grid size must be between \(gridSizeRange.min()!) and \(gridSizeRange.max()!)")
                    .foregroundColor(.red)
                    .font(.headline)
                    .padding(5)
            } else {
                Text(" ")
                    .hidden()
                    .padding(5)
            }
        }
    }
    
    private func Table() -> some View {
        ZStack(alignment: .topLeading) {
            ForEach(viewModel.squares.indices, id: \.self) { index in
                let square = viewModel.squares[index]
                let x = viewModel.squareSize * CGFloat(square.x)
                let y = viewModel.squareSize * CGFloat(square.y)
                let size = viewModel.squareSize * CGFloat(square.size)
                
                Rectangle()
                    .size(width: size, height: size)
                    .fill(square.color)
                    .offset(x: x, y: y)
                    .transition(.scale)
            }
        }
        .frame(width: tableSize, height: tableSize)
        .clipShape(RoundedRectangle(cornerRadius: 8))
        .overlay(RoundedRectangle(cornerRadius: 8).stroke(.black))
    }
    
    private func ListSquares() -> some View {
        VStack {
            Text("Algorithm Results")
                .font(.title)
                .padding(5)
            Text("Best Count squares: \(viewModel.squares.count)")
                .font(.title2)
            Spacer()
            List(viewModel.squares.indices, id: \.self) { index in
                let square = viewModel.squares[index]
                HStack(spacing: 20) {
                    Text("X: \(Int(square.x + 1))")
                    Text("Y: \(Int(square.y + 1))")
                    Text("Size: \(Int(square.size))")
                }
                .padding()
                .font(.title3)
            }
            .frame(width: tableSize / 2, height: tableSize)
            .clipShape(RoundedRectangle(cornerRadius: 8))
        }
    }
}
